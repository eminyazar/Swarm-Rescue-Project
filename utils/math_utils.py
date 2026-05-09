import numpy as np

def distance(p1, p2):
    """
    İki konum (vektör) arasındaki Öklid mesafesini hesaplar.
    """
    return np.linalg.norm(p1 - p2)

def normalize(v):
    """
    Verilen bir vektörü birim vektöre (uzunluğu 1 olan vektör) çevirir.
    Sadece 'yön' bilgisine ihtiyacımız olduğunda kullanacağız.
    """
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def limit(v, max_value):
    """
    Bir vektörün büyüklüğünü (magnitude) sınırlar.
    Bunu robotların MAX_SPEED'i aşmasını veya fiziğe aykırı ani 
    hızlanmalar yapmasını engellemek için kullanacağız.
    """
    norm = np.linalg.norm(v)
    if norm > max_value:
        return (v / norm) * max_value
    return v