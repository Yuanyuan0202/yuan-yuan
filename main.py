from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import subprocess
import shutil
import os
from pathlib import Path
import requests

app = FastAPI()

# 服務靜態文件
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/generate_license/")
def generate_license(
    domain_type: str = Form(...),
    hospital: str = Form(...),
    usage: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    notes: str = Form(...),
    dmi_info: UploadFile = File(...)
):
    print(f"Received: domain_type={domain_type}, hospital={hospital}, usage={usage}, start_date={start_date}, end_date={end_date}, notes={notes}, dmi_info={dmi_info.filename}")
    
    # Save the uploaded file to the designated directory
    UPLOAD_DIRECTORY = Path("uploaded_files")
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIRECTORY / dmi_info.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(dmi_info.file, buffer)
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file.")

    command = f"/root/gen_license/gen_license"
    try:
        # Run the gen_license command with subprocess, provide inputs as string
        result = subprocess.run(command, input=f"n\n{file_path}\n{end_date} 23:59:59\n", text=True, capture_output=True, check=True, shell=True)
        print(result.stdout)
        print(result.stderr)

        # Check if the license files are created
        check_files_command = "ls /root/gen_license/lic.txt /root/gen_license/current_time.txt"
        check_files_result = subprocess.run(check_files_command, shell=True, capture_output=True, text=True)
        print(check_files_result.stdout)
        print(check_files_result.stderr)

        if check_files_result.returncode != 0:
            raise HTTPException(status_code=500, detail="文件生成敗。")

        # Create a tar.gz file
        tar_file = "/root/gen_license/lic_20241231.tgz"
        create_tar_command = f"tar -zcvf {tar_file} /root/gen_license/lic.txt /root/gen_license/current_time.txt"
        subprocess.run(create_tar_command, shell=True, check=True)

        # Ensure tar file is correctly created
        check_tar_command = f"ls {tar_file}"
        tar_check_result = subprocess.run(check_tar_command, shell=True, capture_output=True, text=True)
        print(tar_check_result.stdout)
        print(tar_check_result.stderr)

        if tar_check_result.returncode != 0:
            raise HTTPException(status_code=500, detail="Tar 文件生成失敗。")

        return {"message": "生成成功並上傳到 Redmine。"}

    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e}")
        raise HTTPException(status_code=500, detail=f"License生成失敗：{e}")

    except Exception as e:
        print(f"General error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")

