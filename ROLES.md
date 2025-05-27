# Roles in Propbank API

@paper: Semantic Proto Roles. https://aclanthology.org/Q15-1034.pdf
@chapter: On the Semantic Content of the Notion of ‘Thematic Role’. https://link.springer.com/chapter/10.1007/978-94-009-2723-0_3
@guideline: Propbank Annotation Guidelines. https://verbs.colorado.edu/propbank/EPB-Annotation-Guidelines.pdf

Propbank 3.4 annotations contain 40 roles out of 28638 total.


Key	Role	Count	Percent
PPT	Patient	10715	37.42
PAG	Agent	9494	33.15
GOL	Goal	2482	8.67
PRD	Secondary_Predication	1177	4.11
MNR	Manner	1063	3.71
DIR	Directional	985	3.44
VSP	Verb-specific*	751	2.62
LOC	Locative	618	2.16
EXT	Extent	321	1.12
CAU	Cause	285	1

## Role Descriptions

**Agent**

Subject of transitive verbs.

1. Volitional involvement in the event or state
2. Causing an event or change of state in another participant
3. Movement relative to the position of another participant 

**Patient**

Objects of transitive verbs and the subjects of intransitive verbs called unaccusatives. 

1. Undergo change of state
2. Are causally affected by another participant
3. Are stationary relative to movement of another participant 

**Goal**

This tag is for the goal of the action of the verb. This includes the final destination of motion
verbs and benefactive arguments that receive something, or modifiers that indicate that the
action of the verb was done for someone or something, or on their behalf.

**Manner**
Manner modifiers specify how an action is performed. For example, ‘works well’ is a manner.
Manner tags should be used when an adverb could be an answer to a question starting with
‘How ?’.

**Secondary_Predication**

These are used to show that an adjunct of a predicate is in itself capable of carrying some
predicate structure.
Typical examples include:
1. Resultatives, ‘The boys pinched them dead’ or ‘She kicked [the locker lid]-1 [*-1] shut’
2. Depictives, ‘Rosy-cheeked, Santa came down the chimney’
3. As-phrases, ‘supplied as security in the transaction’
In each of these cases, it is notable that the argument labeled PRD modifies another argument
of the verb (describing its state during or after the event) more than it modifies the verb or
event itself.