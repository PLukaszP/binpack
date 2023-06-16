from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .forms import UploadFileForm
from .models import Batch
from .paker import textFileParser
from .paker import rackPack
import pandas as pd


def upload_file(request):
    context = {}
    context["dataset"] = Batch.objects.all()
    if request.method == "POST":
        context['form'] = UploadFileForm(request.POST, request.FILES)
        if context['form'].is_valid():
            file = request.FILES["file"]
            batch = Batch.objects.create(plik=file)
            batch.save()
            return HttpResponseRedirect("list/")
    else:
        context['form'] = UploadFileForm()
    return render(request, "upload.html", context)


def list_view(request):
    context = {}
    context["dataset"] = Batch.objects.all()
    return render(request, "list_view.html", context)

def detail_view(request, id):
    context = {}
    context["data"] = Batch.objects.get(id=id)
    batch =context["data"]
    dfcols = ['Referencja', 'Szerokosc', 'Wysokosc', 'grubosc', 'bodowa', 'getNr', 'szer', 'wys', 'object']
    df = pd.DataFrame(columns=dfcols)
    with batch.plik.open('r') as f:
        lines = f.readlines()
        df = textFileParser(lines, df, dfcols)
    df_sorted = df.sort_values(by=['wys', 'szer'], ascending=[False, False])
    FreeRowSpace = 4
    context["rackRows"] = rackPack(FreeRowSpace, df_sorted)
    return render(request, "detail_view.html", context)

def delete_view(request, id):
    context ={}
    obj = get_object_or_404(Batch, id=id)
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("/list")
    return render(request, "delete_view.html", context)