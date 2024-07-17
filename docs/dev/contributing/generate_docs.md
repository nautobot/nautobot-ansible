# Generate Docs

The generate_docs.py file is used to generate docs. This page represents some of the how to that was decided in generation outside of the code itself.

## Conversion of Ansible "ShortCodes"

C( ) appears to be a code block within the Ansible docs. These should still be in the documentation for the modules, but in the markdown we convert this over to standard markdown code.

E() covers the environment variables. On top of calling out the environment variables, there is a page that maintains a list of all of the environment variables in the modules in a static page.