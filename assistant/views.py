from django.views import generic


class TopView(generic.TemplateView):
    def get_template_names(self):
        if self.request.user.is_authenticated:
            template_name = 'top_log_in.html'
        else:
            template_name = 'top.html'

        return [template_name]
