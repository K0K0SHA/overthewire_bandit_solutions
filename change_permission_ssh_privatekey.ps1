# Replace 'C:\path\to\bandit17.privatekey' with the actual path to your private key file
$keyFilePath = "E:\bandit\overthewire_bandit_solutions-main"

# Get the SID (Security Identifier) of your user account
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$userSID = $currentUser.User.Value

# Set permissions on the private key file
icacls $keyFilePath /inheritance:r /grant:r "$userSID:(R,W)" /deny "*S-1-1-0:(R,W)"