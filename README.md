# Red-Alert-Windows
- So lets keep this brief
- Red Alert is the name of lockdown script I made for myself, but yall can use it as well
- The idea is that if your computer is compromised your EDR solution just runs the compiled .exe file and then ```RED ALERT``` does the rest
- it pings you in discord using discord webhook with forensic info at the time of compromise and then shuts down your compromised system
- The setup is rather simple , just compile with pyinstaller, set a WEBHOOK variable with the url to your discord webhook (for logs)
- Also it needs admin to run :3

# If you want more details just look at the source
