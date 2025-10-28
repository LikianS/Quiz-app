<template>
  <footer class="bg-custom-dark text-white pt-12 pb-6">
    <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-8">

      <div class="flex flex-col items-center md:items-start text-center md:text-left">
        <img src="@/assets/logo.png" alt="NeuroQuiz Logo" class="h-12 mb-4"/>
        <p class="text-gray-300">NeuroQuiz vous permet de tester vos connaissances sur l'IA et de relever des défis amusants avec vos amis !</p>
      </div>

      <div class="flex flex-col items-center md:items-start text-center md:text-left">
        <h3 class="text-lg font-semibold mb-4">Liens rapides</h3>
        <ul class="space-y-2">
          <li>
            <RouterLink to="/" class="hover:text-main-violet transition">Accueil</RouterLink>
          </li>
          <li>
            <RouterLink to="/new-quiz" class="hover:text-main-violet transition">Quiz</RouterLink>
          </li>
        </ul>
      </div>

      <div class="flex flex-col items-center md:items-start text-center md:text-left">
        <h3 class="text-lg font-semibold mb-4">Suivez-nous</h3>
        <div class="flex space-x-4">
          <a href="https://facebook.com" target="_blank" class="hover:text-main-violet transition">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 fill-current" viewBox="0 0 24 24">
              <path d="M22 12C22 6.48 17.52 2 12 2S2 6.48 2 12c0 5 3.66 9.13 8.44 9.88v-6.99h-2.54V12h2.54V9.84c0-2.5 1.49-3.89 3.77-3.89 1.09 0 2.23.2 2.23.2v2.45h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99C18.34 21.13 22 17 22 12z"/>
            </svg>
          </a>
          <a href="https://twitter.com" target="_blank" class="hover:text-main-violet transition">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 fill-current" viewBox="0 0 24 24">
              <path d="M22.46 6c-.77.35-1.6.58-2.46.69a4.3 4.3 0 0 0 1.88-2.37 8.59 8.59 0 0 1-2.72 1.04 4.28 4.28 0 0 0-7.29 3.9 12.15 12.15 0 0 1-8.82-4.47 4.28 4.28 0 0 0 1.32 5.7 4.24 4.24 0 0 1-1.94-.54v.05a4.28 4.28 0 0 0 3.44 4.19 4.3 4.3 0 0 1-1.93.07 4.28 4.28 0 0 0 3.99 2.97A8.59 8.59 0 0 1 2 19.54a12.09 12.09 0 0 0 6.56 1.92c7.88 0 12.2-6.53 12.2-12.2 0-.19-.01-.37-.02-.56A8.72 8.72 0 0 0 22.46 6z"/>
            </svg>
          </a>
          <a href="https://instagram.com" target="_blank" class="hover:text-main-violet transition">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 fill-current" viewBox="0 0 24 24">
              <path d="M7.75 2h8.5A5.75 5.75 0 0 1 22 7.75v8.5A5.75 5.75 0 0 1 16.25 22h-8.5A5.75 5.75 0 0 1 2 16.25v-8.5A5.75 5.75 0 0 1 7.75 2zm0 1.5A4.25 4.25 0 0 0 3.5 7.75v8.5A4.25 4.25 0 0 0 7.75 20.5h8.5a4.25 4.25 0 0 0 4.25-4.25v-8.5A4.25 4.25 0 0 0 16.25 3.5h-8.5zm8.75 2a.75.75 0 1 1 0 1.5.75.75 0 0 1 0-1.5zm-4.25 1.25a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 1.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7z"/>
            </svg>
          </a>
        </div>
      </div>
    </div>

    <div class="mt-12 border-t border-gray-700 pt-6 text-gray-400 text-sm text-center">
      <p>© 2025 NeuroQuiz. Tous droits réservés.</p>
      <p>
        <RouterLink to="/" class="hover:text-main-violet transition">Politique de confidentialité</RouterLink> | 
        <RouterLink to="/" class="hover:text-main-violet transition">CGU</RouterLink>
      </p>
    </div>
  </footer>
</template>
