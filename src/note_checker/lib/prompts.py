from textwrap import dedent


GRAMMAR_INSTRUCTION = dedent("""
Consider the following markdown document from obsidian. Fix any **major** 
spelling/grammar errors. Do **not** make any significant changes to the content 
of the document beyond small phrasing changes. If there are no changes to be
made, that is perfectly acceptable; in this case, respond with an unmodified document.
                        
Respond with the modified document in Markdown. Your response should **only** contain
the modified markdown; do not provide any additional comments. 
                             
Always respond in plaintext *without* a codeblock.
""")


AUDIT_INSTRUCTION = dedent("""
Consider the following markdown document from obsidian. If you notice any **major**
conceptual errors, add a comment with your recomended amendment in the format of:
                           
> 🤖 (notecheck comment) - TEXT HERE
                           
For example, the following document has a conceptual error:
                           
```md

Pythageran's therom states that:
                           
$$a^2+b^2=c^3$$
                           
```
                           
Your response, for this document, would be:
                           
```md

Pythageran's therom states that:
                           
$$a^2+b^2=c^3$$

> 🤖 (notecheck comment) - The forumla above is incorectly written as $a^2+b^2=\textbf{c^3}$. The power of $c$ should be $2$, not $3$.                          
```
                           
This is a trivial example; some error may be more complex so carefully analyze the document.

Respond with the modified document. If no modificiations are necessary, respond with
the origional document. The *only* changes should be the added comments. In other
words, do not make any changes to the documents elsewhere. Respond in plaintext
*without* a codeblock.                
""")