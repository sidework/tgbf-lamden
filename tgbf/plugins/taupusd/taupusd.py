import decimal
import logging
import tgbf.emoji as emo

from telegram import Update, ParseMode
from telegram.ext import CommandHandler, CallbackContext
from tgbf.lamden.connect import Connect
from tgbf.plugin import TGBFPlugin


class Taupusd(TGBFPlugin):

    def load(self):
        self.add_handler(CommandHandler(
            self.handle,
            self.pusd_callback,
            run_async=True))

    @TGBFPlugin.send_typing
    def pusd_callback(self, update: Update, context: CallbackContext):
        if len(context.args) != 1:
            update.message.reply_text(
                self.get_usage(),
                parse_mode=ParseMode.MARKDOWN)
            return

        amount = context.args[0]

        try:
            amount = float(amount)
        except:
            msg = f"{emo.ERROR} Provided amount not valid!"
            update.message.reply_text(msg)
            return

        contract = self.config.get("contract")
        function = self.config.get("function")

        con_msg = f"{emo.HOURGLASS} Swapping TAU for PUSD..."
        message = update.message.reply_text(con_msg)

        usr_id = update.effective_user.id
        wallet = self.get_wallet(usr_id)
        lamden = Connect(wallet)

        try:
            # Check if contract is approved to spend TAU
            approved = lamden.get_approved_amount(contract)
            approved = approved["value"] if "value" in approved else 0
            approved = approved if approved is not None else 0

            msg = f"Approved amount of TAU for {contract}: {approved}"
            logging.info(msg)

            if amount > float(approved):
                app = lamden.approve_contract(contract)
                msg = f"Approved {contract}: {app}"
                logging.info(msg)
        except Exception as e:
            logging.error(f"Error approving tau_to_pusd: {e}")
            message.edit_text(f"{emo.ERROR} {e}")
            return

        try:
            # Call contract
            swap = lamden.post_transaction(
                stamps=100,
                contract=contract,
                function=function,
                kwargs={"tau_amount": decimal.Decimal(str(amount))}
            )
        except Exception as e:
            logging.error(f"Error calling tau_to_pusd: {e}")
            message.edit_text(f"{emo.ERROR} {e}")
            return

        logging.info(f"Executed tau_to_pusd: {swap}")

        if "error" in swap:
            logging.error(f"tau_to_pusd returned error: {swap['error']}")
            message.edit_text(f"{emo.ERROR} {swap['error']}")
            return

        # Get transaction hash
        tx_hash = swap["hash"]

        # Wait for transaction to be completed
        success, result = lamden.tx_succeeded(tx_hash)

        if not success:
            logging.error(f"tau_to_pusd transaction not successful: {result}")
            message.edit_text(f"{emo.ERROR} {result}")
            return

        #bought_amount = result["result"][result["result"].find("'") + 1:result["result"].rfind("'")]

        link = f'<a href="{lamden.explorer_url}/transactions/{tx_hash}">View Transaction on Explorer</a>'

        message.edit_text(
            f"{emo.DONE} Received PUSD\n{link}",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
