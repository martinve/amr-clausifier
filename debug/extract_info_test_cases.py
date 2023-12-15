amr0 = """
# ::snt Boy ate steak with knife and fork and soup with spoon.
(a / and 
    :op1 (e / eat-01 
        :ARG0 (b / boy) 
        :ARG1 (s / steak) 
        :instrument (a2 / and 
            :op1 (k / knife) 
            :op2 (f / fork))) 
    :op2 (e2 / eat-01 
        :ARG0 b 
        :ARG1 (s2 / soup) 
        :instrument (s3 / spoon)))
"""



amr1 = """
#snt: She works in an office without a window. [isi_0002.599]
(w / work-01
     :ARG0 (s / she)
     :location (o / office
          :ARG0-of (h / have-03
               :polarity -
               :ARG1 (w2 / window))))
"""

amr2 = """
# He was charged with public intoxication and resisting arrest.
(c / charge-05
   :ARG1 (h / he)
   :ARG2 (a / and
            :op1 (i / intoxicate-01
                    :ARG1 h
                    :location (p / public))
            :op2 (r / resist-01
                    :ARG0 h
                    :ARG1 (a2 / arrest-01
                              :ARG1 h))))
"""

amr3 = """
# ::snt Andrea is beautiful, but she is strict.
(c / contrast-01
      :ARG1 (b / beautiful-02
            :ARG1 (p / person
                  :name (n / name
                        :op1 "Andrea")))
      :ARG2 (s / strict
            :domain p))
"""

amr4 = """
# ::snt Man saw a Jaguar driving on a highway.
(s / see-01
      :ARG0 (m / man)
      :ARG1 (d / drive-01
            :ARG0 (c / car-make
                  :wiki "Jaguar_Cars"
                  :name (n / name
                        :op1 "Jaguar"))
            :ARG1 (h / highway)))
"""


amr5 = """
# ::snt Titanic sank in the Atlantic Ocean on 1912.
(s / sink-01
      :ARG1 (s2 / ship
            :wiki "RMS_Titanic"
            :name (n / name
                  :op1 "Titanic"))
      :location (o / ocean
            :wiki "Atlantic_Ocean"
            :name (n2 / name
                  :op1 "Atlantic"
                  :op2 "Ocean"))
      :time (d / date-entity
            :year 1912))
"""

amr6 = """
# ::snt Barack Obama was born in Hawaii.
(b / bear-02
      :ARG1 (p / person
            :wiki "Barack_Obama"
            :name (n / name
                  :op1 "Barack"
                  :op2 "Obama"))
      :location (s / state
            :wiki "Hawaii"
            :name (n2 / name
                  :op1 "Hawaii"))) 
"""

amr7 = """
# ::snt Barack Obama was born in Hawaii.
(b / bear-02
   :ARG1 (p / person
            :wiki "Barack_Obama"
            :name Barack_Obama)
   :location (s / state
                :wiki "Hawaii"
                :name Hawaii)) 
"""

test_case = amr5
