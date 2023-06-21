# AMR Clausifier

AMR clausifier provides environment for parsing the passages in AMR and UD and combining the results.

## Installation and running

1. Install the requirements `pip install -r requirements.txt`
2. Download the model from `https://github.com/bjascob/amrlib-models`. Unpack the model files and place them under `models/model_stog` directory. We have been using `parse_t5` and `parse_xfm_bart_base` for our experiments. If you wish to use text generation functionality, download `generate_t5wtense` model and place it under `models/model_gtos` directory
3. Start the server by running `/server/run_server.py`. You can change the default port by changing the `port` variable in `settins.py`.
4. Open the browser and navigate to `https://localhost:9002`