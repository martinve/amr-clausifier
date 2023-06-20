def get_test_cases():

    graphs = dict()
    sents = dict()

    amr = """
    (s / stab-01
          :ARG0 (p / person
                :name (n / name
                      :op1 "Brutus"))
          :ARG1 (p2 / person
                :name (n2 / name
                      :op1 "Caesar"))
          :instrument (k / knife))
    """
    graphs.update({0: amr})
    sents.update({0: "Brutus stabs Caesar with a knife."})

    amr = """
    (e / elephant
          :domain (p / person
                :name (n / name
                      :op1 "John")))
        """
    graphs.update({1: amr})
    sents.update({1: "John is an elephant."})


    amr = """
    (p / person
          :mod (c / country
                :name (n / name
                      :op1 "Roman"))
          :domain (o / or
                :op1 (p2 / person
                      :name (n2 / name
                            :op1 "Brutus"))
                :op2 (p3 / person
                      :name (n3 / name
                            :op1 "Caesar"))))
        """
    graphs.update({2: amr})
    sents.update({2: "Brutus or Caesar are Romans"})


    amr = """
    (h / have-org-role-91
      :ARG0 (p / person
            :name (n / name
                  :op1 "Donald"
                  :op2 "Trump"))
      :ARG1 (c / country
            :name (n2 / name
                  :op1 "United"
                  :op2 "States"
                  :op3 "of"
                  :op4 "America"))
      :ARG2 (p2 / president))
    """

    graphs.update({3: amr})
    sents.update({3: "Donald Trump was a president of the United States of America."})

    amr = """
    (e / exceed-01
      :ARG0 (d / distance-quantity
              :quant-of (t / tall
                          :domain (p / person :name (n / name :op1 "Ulf"))))
      :ARG1 (d2 / distance-quantity
               :quant-of (t2 / tall
                            :domain (p2 / person :name (n2 / name :op1 "Claire")))))
        """
    graphs.update({4: amr})
    sents.update({4: "Ulf is taller than Claire."})

    amr = """
    (s / sit-01
          :ARG1 (a / apple)
          :ARG2 (t / table))
      """
    graphs.update({5: amr})
    sents.update({5: "Apple sat on the table."})

    amr = """
    (b / big
      :domain (ii / it))
      """
    graphs.update({6: amr})
    sents.update({6: "It was big."})

    amr = """
    (b / big
      :domain (a / amr-unknown))
    """
    graphs.update({7: amr})
    sents.update({7: "What was big?"})

    amr = """
    (m / man
          :domain (p / person
                :name (n / name
                      :op1 "John")))
          """
    graphs.update({8: amr})
    sents.update({8: "John is a man."})

    amr = """
    (m / man
      :mod (b / big)
      :domain (p / person
            :name (n / name
                  :op1 "John")))
                  """
    graphs.update({9: amr})
    sents.update({9: "John is a big man."})

    amr = """
    (e / eat-01
      :ARG0 (b / boy)
      :ARG1 (s / meal)
      :instrument (a / and
            :op1 (k / knife)
            :op2 (s2 / spoon)))
    """
    graphs.update({10: amr})
    sents.update({10: "Boy ate meal with knife and spoon."})

    amr = """
    (a / and
      :op1 (n / nice-01
            :ARG1 (e / elephant))
      :op2 (g / good-02
            :ARG1 e))
            """
    graphs.update({11: amr})
    sents.update({11: "Elephants are nice and good."})

    amr = """
     (b / beat-03
           :ARG0 (c / country :wiki "Germany"
                 :name (n / name :op1 "Germany"))
           :ARG1 (c2 / country :wiki "Netherlands"
                 :name (n2 / name :op1 "Netherlands"))
           :ARG2 (f / final
                 :subevent-of (g / game :wiki "FIFA_World_Cup"
                       :name (n3 / name :op1 "World" :op2 "Cup")
                       :mod (s / soccer)
                       :time (d / date-entity :year 1974)))
           :quant (s2 / score-entity :op1 2 :op2 1))

    """
    graphs.update({12: amr})
    sents.update({12: "In the soccer World Cup final in 1974, Germany beat the Netherlands 2-1."})

    amr = """
    (g / good-off-06
          :ARG1 (l / lad)
          :ARG2-of (h / have-degree-91
                :ARG1 l
                :ARG3 (m / more)
                :ARG4 (o / other
                      :mod (a / all)))
          :time (o2 / once-upon-a-time))
  """


    graphs.update({13: amr})
    sents.update({13: "Once upon a time there was a lad who was better off than all the others."})

    amr = """
    (s / short-06
      :polarity -
      :ARG1 (h / he)
      :ARG2 (m / money)
      :time (e / ever)
      :ARG1-of (c / cause-01
            :ARG0 (h2 / have-03
                  :ARG0 h
                  :ARG1 (p / purse
                        :ARG1-of (e2 / empty-01
                              :time (e3 / ever))))))
    """
    graphs.update({14: amr})
    sents.update({14: "He was never short of money, for he had a purse which was never empty."})

    amr = """
    (h / have-rel-role-91
         :ARG0 (p / person
              :name (n / name
                   :op1 "John"))
         :ARG1 (p2 / person
              :name (n2 / name
                   :op1 "Mary"))
         :ARG2 (h2 / husband)
         :ARG3 (w / wife))
     """
    graphs.update({15: amr})
    sents.update({15: "John and Mary are husband and wife."})

    amr = """
    # ::snt John is a nice man. 
    (m / man 
        :ARG1-of (n / nice-01) 
        :domain (p / person 
            :name (n2 / name :op1 "John")))
    """
    graphs.update({16:amr})
    sents.update({16: "John is a nice man."})


    amr = """
    # ::snt He drives carelessly 
    (d / drive-01
       :ARG0 (h / he)
       :manner (c / care-04
                  :polarity -))
    """
    graphs.update({17: amr})
    sents.update({17: "He drives carelessly."})

    amr = """
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
    graphs.update({18: amr})
    sents.update({18: "Boy ate steak with knife and fork and soup with spoon."})

    amr = """
    (h / have-rel-role-91
      :ARG0 (p / person
            :name (n / name
                  :op1 "Donald"
                  :op2 "Trump"))
      :ARG1 (c / country
            :name (n2 / name
                  :op1 "United"
                  :op2 "States"
                  :op3 "of"
                  :op4 "America"))
      :ARG2 (p2 / president))
    """
    graphs.update({19: amr})
    sents.update({19: "Donald Trump was a president of the United States of America."})


    amr = """
    (l / lad
          :ARG1-of (g / good-03
                :ARG2-of (h / have-degree-91
                      :ARG1 l
                      :ARG3 (m / more)
                      :ARG4 (o / other
                            :mod (a / all)
                        )
                )
    )
    """
    graphs.update({20: amr})
    sents.update({20: "He was never short of money, for he had a purse which was never empty."})

    return graphs, sents



def print_all():
    graphs, sents = get_test_cases()
    for idx in sents.keys():
        print(idx, sents[idx])


def get_example_snt(idx=0):
    graphs, sents = get_test_cases()
    if idx in graphs.keys():
        return graphs[idx], sents[idx]
    return None


if __name__ == "__main__":
    print_all()
