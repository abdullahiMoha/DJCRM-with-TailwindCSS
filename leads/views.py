""" 
Views Module for Leads App
"""
from typing import Any
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Lead,Agent, Category
from .forms import LeadModelForm,CustomUserCreationForm,AssignAgentForm,LeadCategoryUpdateForm

# Create your views here.
class SignupView(generic.CreateView):
    """ 
    CBV for Signup
    """
    template_name="registration/signup.html"
    form_class=CustomUserCreationForm
    
    def get_success_url(self):
        """ 
        Its ets back to the main view of the leads
        """
        return reverse ("login")

class LandingPageView(generic.TemplateView):
    """ 
    CBV for the hiome page of the system
    """
    template_name="landing.html"

class LeadListView(LoginRequiredMixin,generic.ListView):
    """ 
    CBV for displaying list of leads
    """
    template_name="leads/lead_list.html"
    context_object_name="leads"
    
    def get_queryset(self):
        user=self.request.user
        #initial queryset of leads for entire organisation
        if user.is_organisor:
            # pylint: disable=no-member
            queryset=Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=False
            )
        else:
            # pylint: disable=no-member
            queryset=Lead.objects.filter(
                organisation=user.agent.organisation, 
                agent__isnull=False
            )
            #filter for the agent who is logged int
            queryset=queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        user=self.request.user
        context=super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organisor:
            # pylint: disable=no-member
            queryset=Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads":queryset
            })
        return context

class LeadDetailView(LoginRequiredMixin,generic.DetailView):
    """ 
    CBV for displaying a single lead
    """
    template_name="leads/lead_detail.html"
    context_object_name="lead"
    
    def get_queryset(self):
        user=self.request.user
        #initial queryset of leads for entire organisation
        if user.is_organisor:
            # pylint: disable=no-member
            queryset=Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
            #filter for the agent who is logged int
            queryset=queryset.filter(agent__user=user)
        return queryset

class LeadCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView):
    """ 
    CBV for creating a lead
    """
    template_name="leads/lead_create.html"
    form_class=LeadModelForm
    
    def get_success_url(self):
        """ 
        Its ets back to the main view of the leads
        """
        return reverse ("leads:lead-list")
    
    def form_valid(self,form):
        """ 
        Sending email
        """
        lead=form.save(commit=False)
        lead.organisation=self.request.user.userprofile
        lead.save()
        send_mail(
            subject="A lead has been created",
            message="Go to the side to see the new lead",
            from_email="test@test.com",
            recipient_list=["test@test.com"],
        )
        return super(LeadCreateView,self).form_valid(form)

class LeadUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView):
    """ 
    CBV for updating a lead
    """
    template_name="leads/lead_update.html"
    form_class=LeadModelForm
    # pylint: disable=no-member
    def get_queryset(self):
        user=self.request.user
        #initial queryset of leads for entire organisation
        return Lead.objects.filter(organisation=user.userprofile)
    
    def get_success_url(self):
        """ 
        Its Sets back to the main view of the leads
        """
        return reverse ("leads:lead-list")

class LeadDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    """ 
    CBV for deleting a lead
    """
    template_name="leads/lead_delete.html"
    
    def get_success_url(self):
        """ 
        Its Sets back to the main view of the leads
        """
        return reverse ("leads:lead-list")

    def get_queryset(self):
        user=self.request.user
        # pylint: disable=no-member
        #initial queryset of leads for entire organisation
        return Lead.objects.filter(organisation=user.userprofile)

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    """ View for Assigning a lead to an agent"""
    template_name="leads/assign_agent.html"
    form_class=AssignAgentForm
        
    def get_form_kwargs(self,**kwargs):
        kwargs=super(AssignAgentView,self).get_form_kwargs(**kwargs)
            
        kwargs.update({
            "request": self.request
        })
        return kwargs
    
    def get_success_url(self):
        """ 
        Its Sets back to the main view of the leads
        """
        return reverse ("leads:lead-list")
    
    def form_valid(self, form):
        agent=form.cleaned_data["agent"]
        lead=Lead.objects.get(id=self.kwargs["pk"])
        lead.agent=agent
        lead.save()
        return super(AssignAgentView,self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    """ 
    CBV for displaying Categories
    """
    template_name="leads/category_list.html"
    context_object_name="category_list"
    
    def get_context_data(self, **kwargs):
        context=super(CategoryListView, self).get_context_data(**kwargs)
        user=self.request.user
        
        if user.is_organisor:
            # pylint: disable=no-member
            queryset=Lead.objects.filter(
                organisation=user.userprofile, 
            )
        else:
            queryset=Lead.objects.filter(
                organisation=user.agent.organisation, 
            )
        
        context.update({
            "unassigned_lead_count":queryset.filter(category__isnull=True).count(),
            "converted_count":queryset.filter(category__name="Converted").count(),
            "contacted_count":queryset.filter(category__name="Contacted").count(),
            "unconverted_count":queryset.filter(category__name="Unconverted").count()
        })
        return context
    
    def get_queryset(self):
        user=self.request.user
        #initial queryset of leads for entire organisation
        if user.is_organisor:
            # pylint: disable=no-member
            queryset=Category.objects.filter(
                organisation=user.userprofile, 
            )
        else:
            queryset=Category.objects.filter(
                organisation=user.agent.organisation, 
            )
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    """ SHowing up the leads of that category"""
    template_name="leads/category_detail.html"
    context_object_name="category"
    
    def get_queryset(self):
        user=self.request.user
        #initial queryset of leads for entire organisation
        if user.is_organisor:
            # pylint: disable=no-member
            queryset=Category.objects.filter(
                organisation=user.userprofile, 
            )
        else:
            queryset=Category.objects.filter(
                organisation=user.agent.organisation, 
            )
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
    """CBV Updating the category of the lead they belong to"""
    template_name="leads/lead_category_update.html"
    form_class=LeadCategoryUpdateForm
    # pylint: disable=no-member
    def get_queryset(self):
        user=self.request.user
        #initial queryset of leads for entire organisation
        if user.is_organisor:
            # pylint: disable=no-member
            queryset=Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
            #filter for the agent who is logged int
            queryset=queryset.filter(agent__user=user)
        return queryset
    
    def get_success_url(self):
        """ 
        Its Sets back to the main view of the leads
        """
        return reverse ("leads:lead-detail", kwargs={"pk":self.get_object().id})
    