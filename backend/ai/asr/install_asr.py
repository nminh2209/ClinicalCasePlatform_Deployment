"""
Install ASR dependencies and download PhoWhisper model
Run this script to set up the speech recognition backend

Usage:
  cd backend
  python ai/asr/install_asr.py
  
  Or from ai/asr directory:
  python install_asr.py
"""
import sys
import subprocess
import os

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    print_section("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(" ERROR: Python 3.8 or higher is required")
        return False
    
    print(" Python version is compatible")
    return True

def install_dependencies():
    """Install required packages"""
    print_section("Installing ASR Dependencies")
    
    packages = [
        "torch>=2.0.0",
        "transformers>=4.35.0",
        "accelerate>=0.24.0",
        "soundfile>=0.12.0",
        "librosa>=0.10.0",
        "numpy>=1.24.0"
    ]
    
    print("Installing packages:")
    for pkg in packages:
        print(f"  - {pkg}")
    
    print("\nThis may take several minutes...\n")
    
    try:
        # Install PyTorch first (it's large)
        print("Installing PyTorch...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "torch>=2.0.0", "--index-url", "https://download.pytorch.org/whl/cpu"
        ])
        
        # Install other packages
        print("\nInstalling other dependencies...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "transformers>=4.35.0",
            "accelerate>=0.24.0",
            "soundfile>=0.12.0",
            "librosa>=0.10.0",
            "numpy>=1.24.0"
        ])
        
        print("\n All dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n Failed to install dependencies: {e}")
        return False

def download_model():
    """Download PhoWhisper model"""
    print_section("Downloading PhoWhisper Model")
    
    # Set up local cache directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cache_dir = os.path.join(script_dir, "phowhisper")
    
    print("Model: vinai/PhoWhisper-medium")
    print("Size: ~1.5 GB")
    print("This will be downloaded to a local cache directory:")
    print(f"Location: {cache_dir}")
    print("\nBenefit: Easy to delete if you need to free up space!")
    print("\nDownloading... (this may take 5-10 minutes)\n")
    
    try:
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        # Import here after installation
        from transformers import pipeline
        
        # Load the model (this triggers download if not cached)
        print("Loading pipeline...")
        asr_pipeline = pipeline(
            "automatic-speech-recognition",
            model="vinai/PhoWhisper-medium",
            device=-1,  # Use CPU for setup
            cache_dir=cache_dir  # Use local cache
        )
        
        print("\n Model downloaded and cached successfully")
        print(f"Model location: {cache_dir}")
        print(f"Model is ready to use!")
        return True
        
    except Exception as e:
        print(f"\n Failed to download model: {e}")
        print("\nPossible issues:")
        print("  - No internet connection")
        print("  - Firewall blocking downloads")
        print("  - Insufficient disk space (~2GB required)")
        return False

def verify_installation():
    """Verify the installation is working"""
    print_section("Verifying Installation")
    
    try:
        # Import required modules
        import torch
        import transformers
        import soundfile
        import librosa
        
        print(" All imports successful")
        
        # Check PyTorch
        print(f" PyTorch version: {torch.__version__}")
        print(f" Transformers version: {transformers.__version__}")
        
        # Check CUDA availability
        if torch.cuda.is_available():
            print(f" CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("ℹ  CUDA not available - will use CPU (slower but works)")
        
        return True
        
    except Exception as e:
        print(f" Verification failed: {e}")
        return False

def main():
    """Main installation process"""
    print("\n" + "=" * 60)
    print("  ASR Service Installation Script")
    print("  PhoWhisper Model Setup for Vietnamese Speech Recognition")
    print("=" * 60)
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Ask for confirmation
    print("\nThis script will:")
    print("  1. Install PyTorch, Transformers, and audio libraries (~2GB)")
    print("  2. Download PhoWhisper-medium model (~1.5GB)")
    print("  3. Total download: ~3.5GB")
    print("  4. Time required: 10-20 minutes")
    
    response = input("\nContinue? (yes/no): ").lower().strip()
    if response not in ['yes', 'y']:
        print("\nInstallation cancelled.")
        sys.exit(0)
    
    # Step 3: Install dependencies
    if not install_dependencies():
        print("\n Installation failed at dependency installation step")
        sys.exit(1)
    
    # Step 4: Download model
    if not download_model():
        print("\n Installation failed at model download step")
        print("\nYou can retry later by running:")
        print("  cd backend")
        print("  python ai/asr/install_asr.py")
        sys.exit(1)
    
    # Step 5: Verify
    if not verify_installation():
        print("\n  Installation completed but verification failed")
        print("The system may still work, but please check for errors")
        sys.exit(1)
    
    # Success!
    print_section("Installation Complete")
    print(" ASR service is ready to use!")
    print("\nNext steps:")
    print("  1. Start Django server: python manage.py runserver")
    print("  2. Test ASR endpoint: python ai/asr/test_asr_service.py")
    print("  3. Check status: curl http://localhost:8000/api/asr/status/")
    print("\nThe VoiceToText component will now automatically use PhoWhisper")
    print("when Web Speech API is not available (e.g., in Firefox).")
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
