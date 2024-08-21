# Génération Procédurale - Terrain & textures

## Introduction

Voici la définition proposée par wikipédia concernant la génération procédurale:

> En informatique, la génération procédurale (ou modèle procédural)
> est la création de contenu numérique
> (niveau de jeu, modèles 3D, dessins 2D, animation, son, musique,
> histoire, dialogues) à une grande échelle (en grande quantité),
> de manière automatisée répondant à un ensemble de règles définies
> par des algorithmes.

Ces techniques couvrent un vaste champ d'applications :

- cinéma (films d'animation, effets spéciaux),
- jeu vidéo (par exemple pour créer un nouvel environnement à chaque partie),
- scientifique (génération de données variées, par exemple pour entrainer un robot).

Dans mon cas, c'est par le jeu vidéo que je me suis intéressé à ces techniques
pour la première fois.

En particulier sur un projet personnel dans lequel j'ai entrepris de créer 
une variante de la série Civilization dans laquelle la topologie de la planète
devenait une sphère (découpée en hexagones) là où un cylindre était
utilisé dans la série d'origine ... mais c'est un tout autre sujet !

**Problème :**

- Comment générer des continents et des océans, des montagnes, collines et vallées de façon "réaliste" ?
- Comment répartir des forêts, plaines et montagnes (biomes) de manière "crédible" ?

Voici une image illustrant le genre de résultats que j'avais obtenu à l'époque :

- diversité des biomes selon la position géographique (latitude en particulier),
- formes continentales et îles,
- uniformité du maillage partout sur la sphère (y compris aux pôles).

![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/game-2015-01-29-planet.jpg)

Par la suite, j'ai pu mettre en place ces compétences chez Airbus DS,
au sein de l'équipe Image. L'objectif était d'entrainer des modèles
de vision par ordinateur à détecter les zones d'atterrissages propices
à un atterrissage sans danger pour un rover (sur un astéroïde par exemple).

La faible disponibilité d'images réelles de ces corps spatiaux
ouvrait la voie à de la génération procédurale
(combiné à du ray tracing avec l'excellent [SurRender](https://www.airbus.com/en/products-services/space/customer-services/surrendersoftware), développé par Airbus DS).

J'ai donc réutilisé des techniques très similaires pour générer :

- des rochers,
- des cartes d'élévations,
- appliquer des couleurs (textures) au terrain,
- ou encore modéliser des cratères.

<div>
<img src='https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/10125_rocks.jpg' style="width: 49%"/>
<img src='https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/1700_unique_rocks.jpg' style="width: 49%"/>
</div>

Ce genre de techniques offre virtuellement une infinité de données
facilement configurables (distribution des accidents du terrain, montagnes, rochers, etc).

Dans cet article, nous allons nous intéresser aux techniques de
création de contenu 3D et en particulier de terrain.
Nous parlerons également de la génération de textures,
car les mêmes techniques sont souvent utilisées pour les deux problématiques.

Il existe de nombreux articles présentant en détail le fonctionnement
des algorithmes que nous allons évoquer, aussi le choix a été fait de
donner des références de qualité quand elles sont disponibles.

Ce sujet s'adresse donc plutôt à un débutant dans le but de :

- découvrir le vaste champ de techniques nécessaires
  à la création de scènes 3D,
- appliquer ces techniques dans un projet personnel de type "sandbox".

## Carte d'élévation

Si l'on veut générer des terrains, il nous faut d'abord les modéliser.
Nous introduisons la notion de carte d'élévation qui est très largement utilisée.

Une carte d’élévation permet de représenter un terrain (modèle 3D)
dont les sommets (X, Y, Z) sont alignés sur une grille régulière (X, Y).

Les 2 images suivantes illustrent le passage de la carte d'élévation (à gauche)
à sa représentation en 3D (à droite).
La couleur de chaque pixel permet de représenter l'élévation.
Un pixel blanc correspond à un pic, un pixel noir à une vallée et les dégradés de gris
représentent les hauteurs intermédiaires.

![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/noise_Poly_6x5_15x4_10x3_256.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/heightmap3d.png)


**Remarque :**
Cette structure matricielle permet un stockage efficace
de la géométrie (sous forme d'image).
Elle offre donc la possibilité d’utiliser de nombreuses
structures de données (matrice creuse) et algorithmes
existants (filtres : flou, netteté, détection de contour ...).

**Attention :**
Cela induit également des limitations : en particulier,
comme chaque point du plan (X, Y) n’admet qu’une seule hauteur (Z),
il n’est pas possible de représenter des grottes ou des arches avec ce modèle.

Par la suite, on considère la structure suivante représentant un point 3D :

```python
class Point(NamedTuple):
    x: float = 0
    y: float = 0
    z: float = 0
    # with supports for all arithmetic operators (+, -, *, /, %)
```

## Texture

Cette représentation (carte d'élévation) crée un lien naturel entre les terrains et les textures.
Une texture n'est autre qu'une image que l'on plaque à la surface d'un modèle 3D afin de modifier son aspect.

Par exemple, une texture peut déterminer la couleur, les reflets,
la transparence ou encore des micro-reliefs de la matière constituant
l'objet à représenter.

La technique du [Normal Mapping](https://fr.wikipedia.org/wiki/Normal_mapping)
est assez spectaculaire : elle permet de réduire la complexité des modèles 3D tout en gardant
un rendu très détaillé.

Les images suivantes illustrent le passage de la carte d’élévation “brute”
(en niveaux de gris) à une interprétation possible :

- bleu pour les plans d'eau,
- jaune pour les côtes,
- vert pour les plaines,
- marron pour les montagnes,
- blanc pour les sommets enneigés.

![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/noise_height.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/noise_texture.png)

## Techniques de génération

Il existe de nombreuses techniques permettant de générer des terrains
(images) de manière procédurale.

Le résultat final est souvent le résultat d'une suite d'opérations :

- génération aléatoire d'une surface initiale (noise),
- seuillage, déformations et filtres.

### Génération d'une surface (noise)

Voici quelques grandes familles de génération de surface :

- diamond-square (https://en.wikipedia.org/wiki/Diamond-square_algorithm),
- value-noise / gradient-noise (https://en.wikipedia.org/wiki/Value_noise),
- diagrammes de Voronoï (https://en.wikipedia.org/wiki/Worley_noise).

La notion de surface n'est pas limitée à 2 dimensions, il peut s'agir d'une courbe (1 dimension),
d'une surface 2D, 3D ou 4D (la 4ᵉ dimension peut représenter le temps).

**Remarque :**
Avant de créer des techniques plus compliquées,
il est utile de regarder le résultat produit par un simple générateur aléatoire.
L'image suivante illustre ce que l'on appelle un [bruit blanc](https://fr.wikipedia.org/wiki/Bruit_blanc).

![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/white_noise.png)

Ce n'est effectivement pas ce que l'on recherche.
Voici quelques caractéristiques recherchées lors de la génération de terrain:

- continuité (souvent obtenue par interpolation entre deux valeurs aléatoires),
- absence de motifs répétitifs (non-périodicité du signal),
- aspect fractal (auto-similarité du terrain à diverses échelles).

## Value-noise

Parmi les algorithmes évoqués précédemment, `value-noise`
est sans doute le plus simple à implémenter et à comprendre.

Etant donné un tableau `T` de taille `N` initialisé avec des valeurs aléatoires (Cf. bruit blanc ci dessus),
la fonction `value_noise(x: float)` consiste à :

- calculer l'indice `i = floor(x * N)` correspondant à une case de `T`,
- interpoler à partir de `T[i]` et `T[i+1]`

Voici une implémentation de la version en 2 dimensions de cet algorithme.

```python
class ValueNoise:
    def __init__(self, grid_size: int):
        self.size = grid_size
        self.grid = np.random.rand(grid_size, grid_size)

    def noise(self, point: Point) -> float:
        scaled = (point * self.size) % self.size

        x0 = floor(scaled.x)
        y0 = floor(scaled.y)
        x1 = (x0 + 1) % self.size
        y1 = (y0 + 1) % self.size

        v1 = self.grid[x0, y0]
        v2 = self.grid[x0, y1]
        v3 = self.grid[x1, y0]
        v4 = self.grid[x1, y1]

        x = scaled.x % 1
        y = scaled.y % 1

        i1 = interpolate(y, v1, v2)
        i2 = interpolate(y, v3, v4)
        res = interpolate(x, i1, i2)

        return res


def interpolate(t: float, a: float, b: float):
    return a * (1 - t) + b * t
```

Ces quelques images illustrent le résultat de cet algo avec différentes fonctions d'interpolation.

![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/noise_round_128.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/noise_identity_128.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/noise_poly_6x5_15x4_10x3_128.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/noise_inter_cos_128.png)

De gauche à droite :

- grille d'origine,
- interpolation linéaire,
- interpolation polynomiale,
- interpolation basée sur la fonction cosinus

Et voici les diverses fonctions utilisées pour interpoler.

```python
def inter_round(t: float):
    return int(t)


def inter_linear(t: float):
    return t


def inter_poly_6x5_15x4_10x3(t: float):
    return t * t * t * (t * (t * 6 - 15) + 10)


def inter_cos(t: float):
    return .5 * (1 - math.cos(t * math.pi))
```

Les fonctions sont appliquées aux variables `x` et `y` de la fonction `ValueNoise.noise`.
Elles sont construites de manière à envoyer l'intervalle `[0,1]` sur lui-même.

```python
x = scaled.x % 1
y = scaled.y % 1

x = inter_cos(x)
y = inter_cos(y)

i1 = interpolate(y, v1, v2)
i2 = interpolate(y, v3, v4)
res = interpolate(x, i1, i2)
```

**Remarque :**

Cet algorithme est très simple et produit d'assez bons résultats avec une fonction d'interpolation appropriée.
Néanmoins, la structure de la grille de départ reste assez visible.
Dans la section suivante, nous verrons comment gommer ce problème.

## Fractal Brownian Motion

Un [mouvement Brownien fractionnaire (fBm)](https://en.wikipedia.org/wiki/Fractional_Brownian_motion)
est une généralisation du mouvement Brownien.

Le but de cet article n'étant pas l'étude des FBMs,
nous nous contenterons des éléments suivants :

- les FBMs permettent de décrire de nombreux processus observés dans la nature,
- vaste champ d'application : finance (variation de la bourse), physique ...
- propriétés d'auto-similarité.

En ce qui nous concerne, c'est l'aspect fractal (auto-similarité)
qui nous intéresse pour la génération de terrain.

En particulier un algorithme permettant de combiner
un signal avec lui-même en le distordant
(changement de fréquence et d'amplitude).

Le principe est de doubler la fréquence tout en divisant par deux l'amplitude à chaque nouvelle couche.

```python
def fbm(
        noise: Callable[[Point], float],
        layers: int,
        point: Point,
        lacunarity: float = 2,
        power: float = .5
):
    value = 0
    for i in range(layers):
        frequency = lacunarity ** i
        amplitude = power ** i
        value += noise(point * frequency) * amplitude
    return value
```

Voici les résultats obtenus pour `layers=6`
avec les versions précédentes de `value-noise` :

![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_round_128.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_identity_128.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_poly_6x5_15x4_10x3_128.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_inter_cos_128.png)

Bien que des motifs soient toujours présents, il est plus difficile
de percevoir la grille.
De plus, en appliquant un décalage au bruit et en utilisant
un paramètre différent de 2 pour les changements de fréquence,
il est possible d'obtenir des signaux assez différents.

Par exemple voici la même fonction avec `lacunarity=pi/2`.
Les motifs sont beaucoup moins visibles.

![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_1_512.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_3d.png)

En jouant sur le paramètre `power` il est possible d'obtenir des surfaces plus ou moins accidentées.
Les trois images suivantes ont pour paramètre `power` respectif (0.25, 0.5, 0.75).
Un paramètre proche de 0 augmente le poids des basses fréquences
tandis qu'un paramètre proche de 1 augmente le poids des hautes fréquences.

![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_inter_cos_power0.25_256.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_inter_cos_power0.5_256.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_inter_cos_power0.75_256.png)


**Remarque :**
On observe effectivement une grande auto-similarité du terrain, 
mais l'absence de structures particulières ne donne pas un grand intérêt
au terrain ainsi généré.

Il faudra donc faire appel à d'autres procédés pour améliorer la sortie d'un FBM.

En somme, `value-noise` et `fbm` ne sont que des primitives utilisées pour construire un signal plus élaboré.




## Perlin-noise & simplex-noise

Les versions développées par Perlin permettent de réduire les artefacts
liés à l'utilisation d'une grille de valeurs aléatoires.
Leur utilisation est très similaire à celle du `value-noise`,
il suffit de calculer la valeur en un point.

Il existe de nombreuses implémentations de ces algorithmes dans la plupart des languages.
Ces calculs peuvent vite devenir assez coûteux pour de grandes images (en particulier avec l'application du FBM).

## Post-processing & effets spéciaux

Comme nous l'avons vu, les fonctions `noise` et `fbm` permettent
de construire des signaux intéressant pour l'infographie.

Nous présentons maintenant des filtres et autres fonctions permettant
d'altérer le rendu obtenu par les techniques précédentes.

Ainsi, des effets rappelant le bois, le feu, les nuages ou même les vagues
peuvent rapidement être obtenus.

### Terrain accidenté & nuages

Commençons par une fonction très simple avec la valeur absolue.

```python
def rigged(t: float):
    return abs(2 * t - .5)
```

L'application de cette fonction au résultat de `value-noise`
permet de passer de l'image de gauche à celle de droite.

![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_base_256.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_rigged_256.png)

Cet effet est très utile pour créer des chaines de montagnes,
mais aussi des nuages et grâce à son effet "cotonneux".

### Bois et courbes de niveaux

On peut imaginer de nombreux effets basés sur la valeur des pixels d'une image.
L'un d'entre eux est particulièrement intéressant à appliquer sur les
images produites par notre `value-noise`.
Il s'agit d'appliquer la fonction modulo sur son résultat
(tout en normalisant la valeur retournée).

```python
def wood(t: float):
    n = 5.
    k = 1 / n
    return n * (t % k)
```

L'image suivante illustre l'effet obtenu :
des lignes concentriques (mais irrégulière) comme sur du bois.

![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_base_256.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_wood_256.png)

## Conclusion

Il existe beaucoup d'idées que l'on peut appliquer pour générer des cartes d'élévations intéressantes.
Parmi celles-ci, j'aime beaucoup les idées inspirées de l'érosion (cycles pluie / évaporation).
En effet, un post-traitement permet
de simuler l'effet du temps (et des intempéries) sur un relief initial.

Les images ci-dessous montrent l'effet d'une simulation d'érosion sur une carte d'élévation obtenue par un simple fbm.

![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_origin.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_errosion.png)

Pour conclure, la génération procédurale de terrain est un vaste champ
ouvert à l'expérimentation.

Il est très amusant de combiner diverses fonctions pour visualiser 
les résultats dans un moteur 3D.
De plus, il existe de nombreux outils permettant de combiner les blocs constitutifs
du terrain par programmation graphique.
J'espère que cet article vous aura donné envie d'essayer de coder 
vos propres fonctions de génération de terrain dans votre langage préféré.


![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_origin_3d.png)
![](https://assets.tina.io/3d3789e5-e4a7-4eac-aed4-6800e59697a7/generation_procedurale/fbm_errosion_3d.png)




