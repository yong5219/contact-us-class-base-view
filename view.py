# contact-us-class-base-view
class ContactUsCreate(SuccessMessageMixin, CreateView):

    template_name = 'contact_asia/connect-with-us.html'
    model = Country
    form_class = ContactUsForm
    success_message = 'Email sent successfully. Thank you.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, name=self.object.name, email=self.object.email, message=self.object.message)

    def form_valid(self, form):
        client_ip = get_client_ip(self.request)
        form.instance.ip_address = client_ip
        form.instance.to_email = self.slug.email
        return super(ContactUsCreate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        self.slug = get_object_or_404(Country, slug=kwargs['slug'])
        return super(ContactUsCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactUsCreate, self).get_context_data(**kwargs)
        context['country'] = self.slug
        return context
