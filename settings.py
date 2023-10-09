datadir = "../cache/"
dbfile = datadir + "clausifier.sqlite"
protocol = "http"
port = 9002
host = "127.0.0.1"

# model_parse_gsii-v0_1_0   # needs spacy_en_web_sm
# model_parse_spring-v0_1_0 # pip install cached_property
# model_parse_t5-v0_2_0
# model_parse_xfm_bart_base-v0_1_0


amr_server_port = 9003
amr_server_host = "localhost"
amr_parse_model = "model_parse_xfm_bart_large_wiki" # "model_parse_xfm"
amr_multi_sent = True

ud_server_port = 9004
ud_server_host = "localhost"


propbank_corpus = "propbank-3.4"

debug_clauses = False
