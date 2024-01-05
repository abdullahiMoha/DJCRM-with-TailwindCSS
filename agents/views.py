""" 
Any VIEWS for agents app will defined here
"""
import random
from django.core.mail import send_mail
from django.views import generic    
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin

class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
    """ View for displaying list agents"""
    template_name="agents/agent_list.html"
    
    def get_queryset(self):
        """a get querryset for AgentListView() view """
        organisation=self.request.user.userprofile
        # pylint: disable=no-member
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    """ View for Creating new Agent"""
    template_name="agents/agent_create.html"
    form_class=AgentModelForm
    
    def get_success_url(self):
        """ returning to main page of this app"""
        return reverse("agents:agent-list")
    
    def form_valid(self, form):
        """ overiding form_valid() to enter the current user as the oganisation of th agent"""
        user=form.save(commit=False)
        user.is_agent=True
        user.is_organisor=False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        # pylint: disable=no-member
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on DJCRM, please come login to start",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        #agent.organisation=self.request.user.userprofile
        #agent.save()
        return super(AgentCreateView,self).form_valid(form)

class AgentDetailView(OrganisorAndLoginRequiredMixin,generic.DetailView):
    """VIEW for displaying the detail of an agent"""
    template_name="agents/agent_detail.html"
    context_object_name="agent"
    
    def get_queryset(self):
        """a get querryset for AgentListView() view """
        organisation=self.request.user.userprofile
        # pylint: disable=no-member
        return Agent.objects.filter(organisation=organisation)

class AgentUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    """ View for Creating new Agent"""
    template_name="agents/agent_update.html"
    form_class=AgentModelForm
    
    def get_success_url(self):
        """ returning to main page of this app"""
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        """a get querryset for AgentListView() view """
        organisation=self.request.user.userprofile
        # pylint: disable=no-member
        return Agent.objects.filter(organisation=organisation)


class AgentDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    """VIEW for displaying the detail of an agent"""
    template_name="agents/agent_delete.html"
    context_object_name="agent"
    
    def get_success_url(self):
        """ returning to main page of this app"""
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        """a get querryset for AgentListView() view """
        organisation=self.request.user.userprofile
        # pylint: disable=no-member
        return Agent.objects.filter(organisation=organisation)

