## Distribution d’objets dans l’espace

[retour plan](plan.md)

Une scène est généralement constituée des éléments suivants:

- un support (terrain en extérieur ou pièce en intérieur),
- des objets (végétation et rochers en extérieur ou mobilier en intérieur).

De manière générale, il est nécessaire d’habiller une scène en y plaçant différents types d’objets.

### Problème

>Étant donné une scène (2D ou 3D), comment placer un ensemble d’objets (végétation, meubles, rochers, …) de manière harmonieuse ?


Mais que veut dire “harmonieux” ? Voici quelques critères à respecter:

- pas de chevauchement d’objets (respect de l’enveloppe physique),
- absence de motif répétitif, impression d’aléatoire (ex: les arbres ne poussent pas alignés sur une grille - du moins pas naturellement),
- respect de la topologie de la scène (ex: ne pas placer un rocher dans une pente trop raide).

Par conséquent, différents paramètres doivent être pris en compte pour automatiser le placement d’objets:
- nombre d’objets à placer:
  - prédéterminé (par calcul ou par l’utilisateur),
  - calculé itérativement (arrêt de la génération quand un seuil de remplissage est atteint),
- taille des objets (boite englobante, rayon),
- structure/relation entre les objets (ex: les petits objets viennent remplir les espaces entre de gros objets),
- zones interdites (ex: pentes trop raides, murs d’une pièce).

### Approche naïve
>Pour chaque objet à placer, tirer une position aléatoire dans la scène.

**Inconvénients:**

- deux objets peuvent se chevaucher,
- aucune interaction avec la scène (par exemple, un arbre ne doit pas être placé dans une rivière ou un lac).

La plupart des applications concrètes nécessitent de tenir compte des réalités physiques de la scène à construire.

Un algorithme de placement d’objet doit donc:

- permettre d’exclure certaines zones de la scène,
- se souvenir des objets déjà placés.

### Approche "intelligente"

Nous commençons par créer un masque de placement : les objets (par exemple des arbres) sont contraints à la zone sombre. Nous utilisons la carte d’élévation de la scène, en contraignant les objets à être placés dans les plaines.

Il serait possible de prendre en compte le tracé d’une rivière ou tout autre éléments interdisant le placement d’un objet.

<img src="assets/heightmap.png" width="250" />
<img src="assets/background.png" width="250" />

Voici le résultat de la génération de positions en respectant les contraintes suivantes:

- aucun chevauchement d’objet,
- pas d’objet dans la zone claire (orange).


<img src="assets/item-placement-color.gif" width="250" />
<img src="assets/items-position.png" width="250" />


### Exemple

Cette approche offre de nombreuses possibilités, en particulier le fait d’externaliser la construction du masque d’exclusion.
Voici un exemple d’application sur le logo de MonkeyPatch.

<img src="assets/mkp.png" width="250" />
<img src="assets/mkp_mask.png" width="250" />
<img src="assets/mkp_items.png" width="250" />

### Solution proposée

```
def place_items(
    n:int, # nombre d'objets à placer
    allowed_mask:ndarray, # une carte représentant les positions autorisées
    radius: int, # rayon proportionnel à la taille des objets à placer
):
    # dilater les deux masques
    # = exclure un rayon proportionnel à la taille de shape
    dilatated_mask = dilate(allowed_mask, radius)
    dilatated_shape = dilate(shape, radius)

    result = []
    for item in range(N):
        pos = random_position()
        if allowed_mask.contains(pos):
            result.append(pos)
            dilatated_mask.remove(dilatated_shape, at=pos)
    return result
```


