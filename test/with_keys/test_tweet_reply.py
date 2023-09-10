"""
Twitter API changes, reply functionality is no more
"""
# import os
# import unittest
# from bot.twitter_api.tweet_reply import Reply


# class TestTweetReply(unittest.TestCase):
#     def test_tweet_reply(self):

#         request_examples = (
#             "https://github.com/pybamm-team/BattBot/blob/main/REQUEST_EXAMPLES.md"
#         )

#         reply = Reply(testing=True)
#         original_id = reply.retrieve_tweet_id("bot/last_seen_id.txt")

#         self.assertIsInstance(original_id, int)

#         reply.store_tweet_id(original_id, "bot/last_seen_id.txt")
#         retrieved_id = reply.retrieve_tweet_id("bot/last_seen_id.txt")

#         self.assertIsInstance(retrieved_id, int)
#         self.assertEqual(retrieved_id, original_id)

#         tweet_text = (
#             "Compare SPM, SPMe and DFN model with Chen2020 parameters with a 1C"
#             " discharge at 278.15K"
#         )
#         reply.generate_reply(tweet_text, testing=True)

#         assert os.path.exists("plot.gif")
#         os.remove("plot.gif")

#         tweet_text = (
#             "Compare SPM, SPMe with Chen2020 parameters with experiment -"
#             "[('Discharge at C/10 for 10 hours or until 3.3 V', 'Rest for 1 hour', 'Charge at 1 A until 4.1 V', 'Hold at 4.1 V until 50 mA', 'Rest for 1 hour')] * 2"  # noqa
#             " at 278.15K"
#         )
#         reply.generate_reply(tweet_text, testing=True)

#         assert os.path.exists("plot.gif")
#         os.remove("plot.gif")

#         tweet_text = (
#             'Vary "Electrode height [m]" with values [0.3, 0.4, 0.5] with SPM with '
#             "Chen2020 parameters with experiment - "
#             "[('Discharge at C/10 for 10 hours or until 3.3 V', 'Rest for 1 hour', 'Charge at 1 A until 4.1 V', 'Hold at 4.1 V until 50 mA', 'Rest for 1 hour')] * 2"  # noqa
#             " at 278.15K"
#         )
#         reply.generate_reply(tweet_text, testing=True)

#         assert os.path.exists("plot.gif")
#         os.remove("plot.gif")

#         tweet_text = (
#             'Vary "Electrode height [m]" with values [0.3, 0.4, 0.5] with SPM with '
#             "Chen2020 parameters for a discharge of 1C"
#             " discharge at 278.15K"
#         )
#         reply.generate_reply(tweet_text, testing=True)

#         assert os.path.exists("plot.gif")
#         os.remove("plot.gif")

#         tweet_text = (
#             "Compare SPMe and DFN model with Chen2020 parameters with a 1C discharge at"  # noqa: E501
#             " 278.15K"
#         )
#         reply.generate_reply(tweet_text, testing=True)

#         assert os.path.exists("plot.gif")
#         os.remove("plot.gif")

#         tweet_text = (
#             "Compare SPM and DFN model with Marquis2019 parameters with a 1C discharge"
#             " at 278.15K"
#         )
#         reply.generate_reply(tweet_text, testing=True)

#         assert os.path.exists("plot.gif")
#         os.remove("plot.gif")

#         tweet_text = (
#             "Compare SPM and DFN model with Ai2020 parameters with a 0.5C discharge at"
#             " 278.15K"
#         )
#         reply.generate_reply(tweet_text, testing=True)

#         assert os.path.exists("plot.gif")
#         os.remove("plot.gif")

#         tweet_text = (
#             "Compare DFN model with Chen2020 parameters with a 1C discharge at 278.15K"
#         )
#         with self.assertRaisesRegex(
#             Exception,
#             "Please provide atleast 2 models. Some tweet examples -"
#             f" {request_examples}",
#         ):
#             reply.generate_reply(tweet_text, testing=True)

#         tweet_text = "Chen2020 parameters"
#         with self.assertRaisesRegex(
#             Exception,
#             "I'm sorry, I couldn't understand the requested simulation. "
#             + f"Some tweet examples - {request_examples}",
#         ):
#             reply.generate_reply(tweet_text, testing=True)

#         tweet_text = "Compare SPMe and DFN model withChen2020 parameters"
#         with self.assertRaisesRegex(
#             Exception,
#             "Please provide a parameter set in the format - Chen2020. "
#             + f"Some tweet examples - {request_examples}",
#         ):
#             reply.generate_reply(tweet_text, testing=True)

#         tweet_text = (
#             "SPM and DFN model with Ai2020 parameters with a 0.5C discharge at 278.15K"
#         )
#         with self.assertRaisesRegex(
#             Exception,
#             "I'm sorry, I couldn't understand the requested simulation. "
#             + f"Some tweet examples - {request_examples}",
#         ):
#             reply.generate_reply(tweet_text)

#         tweet_text = (
#             "Compare spm and spme at a 6C discharge at fgK with Chen2020 parameters"
#         )
#         with self.assertRaisesRegex(
#             Exception,
#             "Please provide 'Ambient temperature' in the format - "
#             + f"273.15K. Some tweet examples - {request_examples}",
#         ):
#             reply.generate_reply(tweet_text)

#         tweet_text = "Compare spm and spme at a 6C discharge with Chen2020 parameters"
#         with self.assertRaisesRegex(
#             Exception,
#             "Please provide 'Ambient temperature' in the format - "
#             + f"273.15K. Some tweet examples - {request_examples}",
#         ):
#             reply.generate_reply(tweet_text)

#         tweet_text = "Compare spm and spme at 280K with Chen2020 parameters"
#         with self.assertRaisesRegex(
#             Exception,
#             "Please provide 'C rate' in the format - "
#             + f"1C. Some tweet examples - {request_examples}",
#         ):
#             reply.generate_reply(tweet_text)

#         tweet_text = (
#             "Compare spm and spme at 280K at a discharge of fgC with Chen2020"
#             " parameters"
#         )
#         with self.assertRaisesRegex(
#             Exception,
#             "Please provide 'C rate' in the format - "
#             + f"1C. Some tweet examples - {request_examples}",
#         ):
#             reply.generate_reply(tweet_text)

#         tweet_text = (
#             "Compare SPM, SPMe and DFN model with Chen2020 parameters with experiment"
#             " [('Charge at')] at 278.15K"
#         )
#         with self.assertRaises(
#             Exception,
#         ):
#             reply.generate_reply(tweet_text)

#         tweet_text = (
#             'Vary "Electrode Height [m]", [1, 3, 2] SPM with Chen2020 parameters with '
#             "experiment [('Charge at')] at 278.15K"
#         )
#         with self.assertRaises(
#             Exception,
#         ):
#             reply.generate_reply(tweet_text)

#         tweet_text = (
#             'Vary "Electrode height [m]" with values [0.3, 0.4g, 0.5f] with SPM with '
#             "Chen2020 parameters for a discharge of 1C"
#             " discharge at 278.15K"
#         )
#         with self.assertRaises(
#             Exception,
#         ):
#             reply.generate_reply(tweet_text)

#         tweet_text = (
#             'Vary "Negative electrode porosity" with values [0.3, 0.4g, 0.5f] with SPM '  # noqa: E501
#             "with Chen2020 parameters for a discharge of 1C"
#             " discharge at 278.15K"
#         )
#         with self.assertRaises(
#             Exception,
#         ):
#             reply.generate_reply(tweet_text)

#         tweet_text = (
#             'Vary "Negative electrode porosity" with values [0.3, 0.4g, 0.5f] with SPM '  # noqa: E501
#             "with Chen2020 parameters with the experiment "
#             "[('Discharge at C/10 for 10 hours or until 3.3 V', 'Rest for 1 hour', 'Charge at 1 A until 4.1 V', 'Hold at 4.1 V until 50 mA', 'Rest for 1 hour')] * 2"  # noqa: E501
#             " discharge at 278.15K"
#         )
#         with self.assertRaises(
#             Exception,
#         ):
#             reply.generate_reply(tweet_text)

#         tweet_text = (
#             'Vary "Electrode height [m]" with values [0.3, 0.4, 0.5] with SPM and DFN '
#             "with Chen2020 parameters for a discharge of 1C"
#             " discharge at 278.15K"
#         )
#         with self.assertRaises(
#             Exception,
#         ):
#             reply.generate_reply(tweet_text)

#         reply.reply()


# if __name__ == "__main__":
#     unittest.main()
