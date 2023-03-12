class Answer:
    async def answer_callback_query(self, callback_query_id):
        async with aiohttp.ClientSession() as session:
            try:
                await session.post(
                    f"{self.base_url}answerCallbackQuery",
                    params={"callback_query_id": callback_query_id}
                )
            except Exception as e:
                print(f"Error answering callback query: {e}")