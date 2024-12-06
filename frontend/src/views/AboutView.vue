<template>
  <div class="about-wrapper">
    <div class="header-image"></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <!-- Welcome Card -->
      <div class="welcome-card">
        <div class="welcome-content">
          <h1 class="title">
            <v-icon icon="mdi-cat" size="24" class="mr-2"></v-icon>
            Welcome to Kitten Strike!
          </h1>
          <p class="subtitle">Where feline reflexes meet esports!</p>
        </div>
      </div>

      <div class="main-content">
        <!-- Left Card: What is Kitten Strike -->
        <div class="info-card">
          <h2 class="section-title">
            <v-icon icon="mdi-gamepad-variant" class="mr-2"></v-icon>
            What is Kitten Strike?
          </h2>
          <p class="description">
            Imagine Counter-Strike, but instead of regular characters, you have kittens with tactical vests and laser pointers! 🐱
            This is a game where precision is as important as the afternoon nap, and strategy is more delicious than a bowl of tuna.
          </p>
          <div class="features">
            <div class="feature-item">
              <v-icon icon="mdi-target" color="#42DDF2FF"></v-icon>
              <span>Precise aiming with laser pointers</span>
            </div>
            <div class="feature-item">
              <v-icon icon="mdi-run-fast" color="#42DDF2FF"></v-icon>
              <span>Feline reflexes and acrobatic skills</span>
            </div>
            <div class="feature-item">
              <v-icon icon="mdi-account-group" color="#42DDF2FF"></v-icon>
              <span>Team play and tactical purring</span>
            </div>
          </div>
        </div>

        <!-- Right Card: Tournament Types -->
        <div class="tournament-card">
          <h2 class="section-title">
            <v-icon icon="mdi-trophy" class="mr-2"></v-icon>
            Tournament Types
          </h2>
          <div class="tournament-types">
            <div class="tournament-type">
              <v-icon icon="mdi-tournament" color="#FED854FF"></v-icon>
              <div class="tournament-info">
                <h3>Single Elimination</h3>
                <p>Like a game of cat and mouse - one mistake and you're out! Perfect for dramatic moments and epic finals.</p>
              </div>
            </div>
            <div class="tournament-type">
              <v-icon icon="mdi-refresh" color="#FED854FF"></v-icon>
              <div class="tournament-info">
                <h3>Round Robin</h3>
                <p>Everyone plays against everyone - like a cat party where every kitty meets each other! Ideal for determining the true alpha cat.</p>
              </div>
            </div>
            <div class="tournament-type">
              <v-icon icon="mdi-lightning-bolt" color="#FED854FF"></v-icon>
              <div class="tournament-info">
                <h3>One Off Match</h3>
                <p>Quick and intense format - like a lightning-fast scramble for the last can of tuna!</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Bottom Card: Prizes -->
        <div class="prizes-card">
          <h2 class="section-title">
            <v-icon icon="mdi-gift" class="mr-2"></v-icon>
            Prizes
          </h2>
          <p class="description">
            In Kitten Strike, prizes aren't just trophies - they're real treasures! Winners receive prestigious "Kitty Kibbles" - special currency that can be used to purchase equipment, cosmetic items, and many other feline goodies!
          </p>
          <div class="prizes-list">
            <div class="prize-item">
              <v-icon icon="mdi-crown" color="#FED854FF"></v-icon>
              <span>1st Place: Golden Fish Bowl Trophy</span>
            </div>
            <div class="prize-item">
              <v-icon icon="mdi-medal" color="#C0C0C0"></v-icon>
              <span>2nd Place: Silver Milk Saucer</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about-wrapper {
  min-height: 100vh;
  position: relative;
}

.header-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px;
  background-image: url('@/assets/top-image.png');
  background-size: cover;
  background-position: center;
  z-index: 1;
  opacity: 0.6;
}

.header-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 400px;
  background: linear-gradient(
    to bottom,
    rgba(23, 28, 38, 0) 0%,
    rgba(23, 28, 38, 0.8) 20%,
    rgba(23, 28, 38, 1) 40%
  );
  z-index: 2;
}

.content-wrapper {
  position: relative;
  z-index: 3;
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
  margin-left: 400px;
}

.welcome-card,
.info-card,
.tournament-card,
.prizes-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42DDF2FF;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  padding: 24px;
  margin-bottom: 24px;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
}

.welcome-content {
  text-align: center;
}

.title {
  color: #42DDF2FF;
  font-size: 2rem;
  margin: 0;
}

.subtitle {
  color: #FED854FF;
  font-size: 1.2rem;
  margin-top: 8px;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.prizes-card {
  grid-column: 1 / -1;
}

.section-title {
  color: #42DDF2FF;
  font-size: 1.5rem;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
}

.description {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 20px;
  line-height: 1.6;
}

.features,
.tournament-types,
.prizes-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feature-item,
.tournament-type,
.prize-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  background: rgba(66, 221, 242, 0.1);
  transition: all 0.2s;

}

.feature-item {
  color: white;
}

.tournament-type {
  background: rgba(254, 216, 84, 0.1);
}

.tournament-info {
  flex: 1;
}

.tournament-info h3 {
  color: #FED854FF;
  margin: 0 0 4px 0;
  font-size: 1.2rem;
}

.tournament-info p {
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-size: 0.9rem;
}

.prize-item {
  background: rgba(254, 216, 84, 0.1);
  color: #FED854FF;
}

.prize-item:last-child {
  background: rgba(192, 192, 192, 0.1);
  color: #C0C0C0;
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}
</style>

<script setup lang="ts">
</script>
