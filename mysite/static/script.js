document.addEventListener('DOMContentLoaded', () => {
    console.log("Script loaded");

    // Animation for the shield icon
    const shieldIcon = document.querySelector('.shield-icon');
    let rotation = 0;
    function animateShield() {
        rotation = (rotation + 1) % 360;
        shieldIcon.style.transform = `rotate(${Math.sin(rotation * Math.PI / 180) * 2}deg)`;
        requestAnimationFrame(animateShield);
    }
    animateShield();
});
