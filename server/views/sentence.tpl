% rebase('base.tpl', title="Experiment Details")

% import pickle
% from udutil import format_ud
% import formatter

<h1>Sentence Parse</h1>

{{ sentence.text }}

<div class="my-4">
    <a href="/passage/{{sentence.experiment.id}}">Passage</a>
    <a href="/sentences/{{sentence.id}}/logic">Update Logic</a>
</div>


<div class="row">
    <div class="col">
        <h3>AMR Parse</h3>
        <code>{{ sentence.parse_amr }}</code>
    </div>
    <div class="col">
        <h3>UD Parse</h3>
        <code>{{ "\n".join(format_ud(pickle.loads(sentence.parse_ud))) }}</code>
    </div>
</div>

<div class="row">
    <div class="col">
        <h3>Logic</h3>

        <!--

        -->
        <code>{{ formatter.format_logic(sentence.simpl_logic) }}</code>

        <!--
        <h4>Previous approach</h4>
        <code class="mt-4">{{ formatter.format_logic(sentence.logic) }}</code>
        -->
    </div>
    <div class="col">
        <h3>Context</h3>
        <code>{{ formatter.format_json(sentence.context) }}</code>
    </div>
</div>

