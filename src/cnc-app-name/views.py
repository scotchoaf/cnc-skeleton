# Copyright (c) 2018, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: $YOURNAME and $EMAIL

"""
Palo Alto Networks cnc-skeleton

This software is provided without support, warranty, or guarantee.
Use at your own risk.
"""

from django import forms
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect

# Every app will need to import at least the CNCBaseFormView
from pan_cnc.views import CNCBaseFormView, ProvisionSnippetView


# All class attributes can be defined here or in the .pan-cnc.yaml
# In this case, we have defined class level attributes there. This makes it possible to
# create apps while writing no code at all. Just create a view in the .pan-cnc.yaml based on a
# CNCBaseFormView and configure the attributes as needed.
# If you want additional logic, then you subclass the CNCBaseFormView and add your logic there.
# The two main methods to override are 'generate_dynamic_form' and 'form_valid'.
#
# generate_dynamic_form gets called before the web form is created and displayed to the user
#
# form_valid is called after they submit the form
#

class ExampleAppView(CNCBaseFormView):

    def form_valid(self, form):
        # we now have the form from the user, let's get some values to perform some logic
        # every variable entered by the user is saved in the user session. We can access it using this
        # convenience method:
        var_name = self.get_value_from_workflow('var_name', 'DEFAULT_IF_NOT_FOUND')
        var_name_again = self.get_value_from_workflow('var_name_again', 'DEFAULT_IF_NOT_FOUND')

        # silly exercise to just upper case the value entered by the user
        var_name_upper = str(var_name).upper()

        var_name_again_reverse = str(var_name_again)[::-1]

        # now, save the values back to the workflow
        self.save_value_to_workflow('var_name', var_name_upper)
        self.save_value_to_workflow('var_name_again', var_name_again_reverse)

        # and call our super to continue processing
        return super().form_valid(form)


# Again override the baseformview as we are only building a workflow here
class ExampleAppPasswordView(ProvisionSnippetView):

    def get_snippet(self):
        return self.snippet

    # this method allows us to customize what is shown to the user beyond what is present in the loaded skillet
    # 'variables' section

    def generate_dynamic_form(self):
        # let's first get the generated from from our base class
        dynamic_form = super().generate_dynamic_form()

        dynamic_form.fields['password_2'] = forms.CharField(widget=forms.PasswordInput(render_value=True),
                                                            initial='')

        return dynamic_form

    # the user has now completed the form and we have the results
    def form_valid(self, form):
        # Everything the user has entered will be avabile here in the 'workflow'
        workflow = self.get_workflow()

        # get the values from the user submitted here
        var_name = workflow.get('var_name')
        var_name_again = workflow.get('var_name_again')
        example_password = workflow.get('example_password')

        # we can also get any items we added to the form dynamically
        password_2 = workflow.get('password_2')

        if example_password != password_2:
            # Send an error message back to the user
            messages.add_message(self.request, messages.ERROR, 'Passwords do not match!')
            return HttpResponseRedirect('workflow00')

        print('Got some vars here!')
        print(f'Found value for var_name: {var_name}')
        print(f'Found another value for var_name_again {var_name_again}')
        return super().form_valid(form)

