import os
import pybamm
import unittest
from bot.twitter_api.upload import Upload
from bot.plotting.random_plot_generator import random_plot_generator


class TestUpload(unittest.TestCase):
    def test_upload(self):
        return_dict = {}
        random_plot_generator(
            return_dict,
            "model comparison",
            {
                "chemistry": pybamm.parameter_sets.Chen2020,
                "models_for_comp": {
                    0: pybamm.lithium_ion.DFN(),
                    1: pybamm.lithium_ion.SPM(),
                },
                "is_experiment": False,
                "cycle": None,
                "number": None,
                "param_to_vary_info": None,
                "bounds": None,
                "reply_overrides": None,
            },
        )

        plot = "plot.gif"
        total_bytes = os.path.getsize(plot)

        upload = Upload(plot, total_bytes)
        upload.upload_init()
        upload.upload_append()
        upload.upload_finalize()

        os.remove(plot)

        return_dict = {}
        random_plot_generator(
            return_dict,
            "degradation comparison (summary variables)",
            {
                "chemistry": pybamm.parameter_sets.Chen2020,
                "model": pybamm.lithium_ion.DFN(),
                "cycle": [
                    (
                        "Discharge at C/10 for 10 hours or until 3.3 V",
                        "Rest for 1 hour",
                        "Charge at 1 A until 4.1 V",
                        "Hold at 4.1 V until 50 mA",
                        "Rest for 1 hour",
                    )
                ],
                "number": 2,
            },
        )

        plot = "plot.png"
        total_bytes = os.path.getsize(plot)

        upload = Upload(plot, total_bytes)
        upload.upload_init()
        upload.upload_append()
        upload.upload_finalize()

        os.remove(plot)


if __name__ == "__main__":
    unittest.main()
