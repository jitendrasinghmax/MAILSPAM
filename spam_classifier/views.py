from django.shortcuts import render
from django.http import JsonResponse
from .ml_utils import SpamClassifier
from .models import EmailPrediction

classifier = SpamClassifier()

def predict_spam(request):
    if request.method == 'POST':
        email_text = request.POST.get('email_text', '')
        if email_text:
            # Get prediction
            result = classifier.predict(email_text)
            
            # # Save prediction
            # EmailPrediction.objects.create(
            #     email_text=email_text,
            #     prediction=bool(result)
            # )
            
            return JsonResponse({
                'is_spam': bool(result),
                'message': 'Spam' if result == 1 else 'Not Spam'
            })
        
    return render(request, 'predict.html')

