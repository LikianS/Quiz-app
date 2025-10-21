<template>
    <div class="login-container">
        <h2>Connexion Admin</h2>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label for="password">Mot de passe :</label>
                <input
                    id="password"
                    type="password"
                    v-model="password"
                    autocomplete="current-password"
                    placeholder="Entrez votre mot de passe"
                />
            </div>
            <button type="submit" class="login-button">Connexion</button>
            <p v-if="error" class="error-message">Mauvais mot de passe</p>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router' // <-- ajoute ceci

const password = ref('')
const error = ref(false)
const ADMIN_PASSWORD = 'iloveflask'
const router = useRouter() // <-- ajoute ceci

function handleLogin() {
    if (password.value === ADMIN_PASSWORD) {
        error.value = false
        router.push('/admin') 
    } else {
        error.value = true
    }
}
</script>

<style scoped>
/* Conteneur principal */
.login-container {
    max-width: 400px;
    margin: 60px auto;
    padding: 32px;
    border: 1px solid #ddd;
    border-radius: 12px;
    background: #ffffff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
    font-family: 'Arial', sans-serif;
}

/* Titre */
h2 {
    font-size: 24px;
    margin-bottom: 24px;
    color: #180000;
}
/* Formulaire */
.form-group {
    margin-bottom: 16px;
    text-align: left;
}

label {
    display: block;
    font-size: 14px;
    margin-bottom: 8px;
    color: #0f0000;
}

input {
    width: 100%;
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 8px;
    outline: none;
    transition: border-color 0.3s;
}

input:focus {
    border-color: #007bff;
}

/* Bouton */
.login-button {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.login-button:hover {
    background-color: #0056b3;
}

/* Message d'erreur */
.error-message {
    color: #d32f2f;
    margin-top: 12px;
    font-size: 14px;
}

/* Responsive */
@media (max-width: 480px) {
    .login-container {
        padding: 24px;
    }

    h2 {
        font-size: 20px;
    }

    .login-button {
        font-size: 14px;
    }
}
</style>