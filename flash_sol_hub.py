from pyvirtualdisplay import Display
display = Display(visible=0, size=(1024, 768))
display.start()

import tkinter as tk
import web3
from web3 import Web3
import json
import os

class FlashSOLHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Flash SOL Hub")
        self.root.geometry("400x300")

        self.bsc = Web3(Web3.HTTPProvider("https://data-seed-prebsc-1-s1.binance.org:8545")) # BSC Testnet
        self.private_key = "0xa03bda0794c69aa57aee27718167645b1aab78f5183bb5b7cb6eae73293dfc7c" # Replace with test wallet key

        self.contracts = {
            "BSC": "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4", # Replace after deploy
        }
        self.abi = json.loads(open("FlashSOL.abi").read()) # From compilation

        tk.Label(root, text="Flash SOL Generator").pack(pady=10)
        tk.Label(root, text="Recipient Address:").pack()
        self.recipient = tk.Entry(root)
        self.recipient.pack()

        tk.Label(root, text="Amount (FSOL):").pack()
        self.amount = tk.Entry(root)
        self.amount.pack()

        tk.Label(root, text="Chain:").pack()
        self.chain = tk.StringVar(value="BSC")
        tk.OptionMenu(root, self.chain, "BSC").pack() # Solana skipped for Win 7

        tk.Button(root, text="Generate Flash SOL", command=self.generate).pack(pady=20)
        self.status = tk.Label(root, text="Ready...")
        self.status.pack()

    def generate(self):
        recipient = self.recipient.get()
        amount = int(self.amount.get()) * 10**9 # 9 decimals
        chain = self.chain.get()

        if not recipient or not amount:
            messagebox.showerror("Error", "Fill all fields!")
            return

        try:
            w3 = self.bsc
            account = w3.eth.account.from_key(self.private_key)
            w3.eth.default_account = account.address
            contract = w3.eth.contract(address=self.contracts[chain], abi=self.abi)

            tx = contract.functions.flashMint(recipient, amount).transact({
                "from": account.address,
                "gas": 200000,
            })
            w3.eth.wait_for_transaction_receipt(tx)
            self.status.config(text=f"Minted {amount / 10**9} FSOL on {chain}! Tx: {tx.hex()}")

            tx = contract.functions.transfer(recipient, amount // 2).transact({"from": account.address})
            w3.eth.wait_for_transaction_receipt(tx)
            self.status.config(text=f"Sent {amount / 2 / 10**9} FSOL to {recipient}!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashSOLHub(root)
    root.mainloop()
