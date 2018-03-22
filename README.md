# Busfit

Busfit est une application interactive qui utilise la technologie [Kinect](https://en.wikipedia.org/wiki/Kinect) afin de vérifier que l'utilisateur
reproduit les mouvements de fitness montrés à l'écran. *Busfit* est pensée pour être utilisée par le biais des nouvelles bornes interactives des abribus de la ville 
de Montréal. Les usagers de la STM pourraient faire un peu de sport en attendant le bus !

## Client de jeu
Le client de jeu est une application web Vue.js reliée en temps réel à un serveur NodeJS par une connexion WebSocket (socket.io).
Le serveur NodeJS consomme les données produites par le programme kinect.py que nous avons développée pour interpréter les données de **positions de joints du squelette** de telle sorte à reconnaitre les mouvements de fitness. 
