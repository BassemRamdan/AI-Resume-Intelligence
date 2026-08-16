import { ResumeAnalysisProvider } from "./ResumeAnalysisProvider";
import { spawn } from "child_process";
import path from "path";
import os from "os";
import fs from "fs/promises";
import { v4 as uuidv4 } from "uuid";
import { GroqProvider } from "./GroqProvider";

export class LocalResumeProvider implements ResumeAnalysisProvider {
  private getPythonExec(): string {
    const venvPython = path.join(process.cwd(), 'venv', 'Scripts', 'python.exe');
    // Check if venv python exists, else use global python
    try {
      const fsSync = require('fs');
      if (fsSync.existsSync(venvPython)) {
        return venvPython;
      }
    } catch(e) {}
    
    return 'python';
  }

  private async runPythonScript(scriptPath: string, args: string[], startMarker: string, endMarker: string): Promise<any> {
    return new Promise((resolve, reject) => {
      const pythonExec = this.getPythonExec();
      const pyProcess = spawn(pythonExec, [scriptPath, ...args]);

      let output = '';
      let errorOutput = '';

      pyProcess.stdout.on('data', (data) => {
        output += data.toString();
      });

      pyProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      pyProcess.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(`Python Error: ${errorOutput}`));
          return;
        }

        const startIndex = output.indexOf(startMarker);
        const endIndex = output.indexOf(endMarker);

        if (startIndex !== -1 && endIndex !== -1) {
          const jsonStr = output.substring(startIndex + startMarker.length, endIndex).trim();
          try {
            const result = JSON.parse(jsonStr);
            resolve(result);
          } catch (e) {
            reject(new Error(`Invalid JSON response: ${jsonStr}`));
          }
        } else {
          reject(new Error(`Markers not found in output: ${output}`));
        }
      });
    });
  }

  async extractProfile(fileBuffer: Buffer, filename: string): Promise<any> {
    const tempDir = os.tmpdir();
    const pdfPath = path.join(tempDir, `resume_${uuidv4()}.pdf`);
    await fs.writeFile(pdfPath, fileBuffer);

    const pythonScript = path.join(process.cwd(), 'lib', 'ai', 'extract_resume.py');
    try {
      const rawProfile = await this.runPythonScript(
        pythonScript, 
        [pdfPath], 
        '===START===', 
        '===END==='
      );
      
      const groq = new GroqProvider();
      const cleanedProfile = await groq.cleanProfile(rawProfile);
      
      // Inject filename
      cleanedProfile.filename = filename;
      return cleanedProfile;
    } finally {
      try {
        await fs.unlink(pdfPath);
      } catch (e) {
        console.error("Failed to delete temp PDF", e);
      }
    }
  }



  async generateCareerMap(candidateProfile: any): Promise<any> {
    const tempDir = os.tmpdir();
    const jobId = uuidv4();
    const profileFile = path.join(tempDir, `profile_career_${jobId}.json`);

    await fs.writeFile(profileFile, JSON.stringify(candidateProfile), 'utf-8');

    const pythonScript = path.join(process.cwd(), 'lib', 'ai', 'career_engine.py');
    try {
      return await this.runPythonScript(
        pythonScript, 
        [profileFile], 
        '===START===', 
        '===END==='
      );
    } finally {
      try {
        await fs.unlink(profileFile);
      } catch (e) {
        console.error("Failed to delete temp file", e);
      }
    }
  }
}
