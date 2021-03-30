# -*- coding: utf-8 -*- 
'''
Created on Apr 28, 2014

@author: Muneeb
'''
from django.utils import timezone as dj_datetime
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
import time
from django.core.exceptions import ValidationError
import re

def file_upload_to(instance, filename):
    return '/'.join([instance.__class__.__name__, unicode(dj_datetime.now().strftime('%Y/%m/%d')),
            unicode( int(time.time()))+filename])
    
    
def validate_number(value):
    result = re.match('^[-\d]+$', value)
    if result is None:
        raise ValidationError('%s is not a valid telephone number' % value)
    else:
        return value    
    

STATES = Choices((u'Álava', _(u'Álava')),
                (u'Albacete', _(u'Albacete')),
                (u'Alicante/Alacant', _(u'Alicante/Alacant')),
                (u'Almería', _(u'Almería')),
                (u'Asturias', _(u'Asturias')),
                (u'Ávila', _(u'Ávila')),
                (u'Badajoz', _(u'Badajoz')),
                (u'Barcelona', _(u'Barcelona')),
                (u'Burgos', _(u'Burgos')),
                (u'Cáceres', _(u'Cáceres')),
                (u'Cádiz', _(u'Cádiz')),
                (u'Castellón/Castelló', _(u'Castellón/Castelló')),
                (u'Ceuta', _(u'Ceuta')),
                (u'Ciudad Real', _(u'Ciudad Real')),
                (u'Córdoba', _(u'Córdoba')),
                (u'Cuenca', _(u'Cuenca')),
                (u'Girona', _(u'Girona')),
                (u'Las Palmas', _(u'Las Palmas')),
                (u'Granada', _(u'Granada')),
                (u'Guadalajara', _(u'Guadalajara')),
                (u'Huelva', _(u'Huelva')),
                (u'Huesca', _(u'Huesca')),
                (u'Illes Balears', _(u'Illes Balears')),
                (u'Jaén', _(u'Jaén')),
                (u'A Coruña', _(u'A Coruña')),
                (u'La Rioja', _(u'La Rioja')),
                (u'León', _(u'León')),
                (u'Lleida', _(u'Lleida')),
                (u'Madrid', _(u'Madrid')),
                (u'Málaga', _(u'Málaga')),
                (u'Melilla', _(u'Melilla')),
                (u'Murcia', _(u'Murcia')),
                (u'Navarra', _(u'Navarra')),
                (u'Ourense', _(u'Ourense')),
                (u'Palencia', _(u'Palencia')),
                (u'Pontevedra', _(u'Pontevedra')),
                (u'Salamanca', _(u'Salamanca')),
                (u'Segovia', _(u'Segovia')),
                (u'Sevilla', _(u'Sevilla')),
                (u'Soria', _(u'Soria')),
                (u'Tarragona', _(u'Tarragona')),
                (u'Santa Cruz de Tenerife', _(u'Santa Cruz de Tenerife')),
                (u'Teruel', _(u'Teruel')),
                (u'Toledo', _(u'Toledo')),
                (u'Valencia/Valéncia', _(u'Valencia/Valéncia')),
                (u'Valladolid', _(u'Valladolid')),
                (u'Vizcaya', _(u'Vizcaya')),
                (u'Zamora', _(u'Zamora')),
                (u'Zaragoza', _(u'Zaragoza')),
                )


