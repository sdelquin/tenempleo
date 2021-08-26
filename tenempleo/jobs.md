Hola {{ username }},

Hemos encontrado algunas ofertas de empleo que te pueden resultar de interés:

{% for job_offer in job_offers %}

**{{ job_offer['shortText'] }}**

- Fecha de publicación: {{ job_offer['date'] }}
- Descripción: {{ job_offer['longText']|replace('\n', ' | ') }}
{% if job_offer['email'] %}
- Email de contacto: {{ job_offer['email'] }}
{% endif %}
{% if job_offer['urlList'] %}
- Enlace: {{ job_offer['urlList'][0] }}
{% endif %}
{% if job_offer['phoneNumber'] %}
- Teléfono: {{ job_offer['phoneNumber'] }}
{% endif %}

{% endfor %}
