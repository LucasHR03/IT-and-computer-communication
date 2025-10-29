from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Bruger, Rolle


# ---------- LOGIN ----------
def login_view(request):
    if request.method == 'POST':
        brugernavn = request.POST.get('username')
        adgangskode = request.POST.get('password')

        user = authenticate(request, username=brugernavn, password=adgangskode)

        if user is not None:
            login(request, user)
            messages.success(request, f"Velkommen, {user.navn}!")
            return redirect('dashboard')  # ← Skift evt. til din dashboard-URL
        else:
            messages.error(request, 'Ugyldigt brugernavn eller adgangskode.')

    return render(request, 'brugere/login.html')


# ---------- LOGOUT ----------
def logout_view(request):
    logout(request)
    messages.info(request, "Du er nu logget ud.")
    return redirect('brugere:login')


# ---------- REGISTRERING ----------
def register_view(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        brugernavn = request.POST.get('username')
        adgangskode = request.POST.get('password')
        role_id = request.POST.get('role')

        # valider input
        if not all([full_name, brugernavn, adgangskode, role_id]):
            messages.error(request, "Alle felter er påkrævet.")
            return redirect('brugere:opret')

        try:
            rolle = Rolle.objects.get(id=int(role_id))

            Bruger.objects.create_user(
                brugernavn=brugernavn,
                adgangskode=adgangskode,
                navn=full_name,
                rolle=rolle
            )

            messages.success(request, "Bruger oprettet! Du kan nu logge ind.")
            return redirect('brugere:login')

        except Rolle.DoesNotExist:
            messages.error(request, "Den valgte rolle findes ikke.")
            return redirect('brugere:opret')

def register_view(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        brugernavn = request.POST.get('username')
        adgangskode = request.POST.get('password')
        role_id = request.POST.get('role')

        # valider input
        if not all([full_name, brugernavn, adgangskode, role_id]):
            messages.error(request, "Alle felter er påkrævet.")
            return redirect('brugere:opret')

        try:
            rolle = Rolle.objects.get(id=int(role_id))

            Bruger.objects.create_user(
                brugernavn=brugernavn,
                adgangskode=adgangskode,
                navn=full_name,
                rolle=rolle
            )

            messages.success(request, "Bruger oprettet! Du kan nu logge ind.")
            return redirect('brugere:login')

        except Rolle.DoesNotExist:
            messages.error(request, "Den valgte rolle findes ikke.")
            return redirect('brugere:opret')

    # GET-request → vis formular
    roller = Rolle.objects.all().order_by('navn')
    return render(request, 'brugere/opret.html', {'roller': roller})



