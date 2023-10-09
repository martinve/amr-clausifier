% rebase('base.tpl', title='Page Title')

% from amrutil import format_amr
% from udutil import format_ud

<h1>Parse Result</h1>

<table class="u-full-width">
    <tbody>
    % for snt in data["sentences"]:
        <tr>
            <td>{{ snt["sentence"] }}</td>
            <td>
                <pre><code>{{ format_amr(snt["semparse"]["amr"]) }}</code></pre>
            </td>
            <td>
                <pre><code>{{ "\n".join(format_ud(snt["semparse"]["ud"])) }}</code></pre>
            </td>
        </tr>
    % end
    </tbody>
</table>

<a class="button" href="/">Back</a>
<a class="button button-primary u-pull-right" href="/save">Save to Database</a>


<pre>
{{ fmtdata }}
</pre>
