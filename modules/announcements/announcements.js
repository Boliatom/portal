class AnnouncementsModule extends HTMLElement {
  connectedCallback() {
    const items = [
      { title: 'Пятница короткая', details: 'Работаем до 16:00.' },
    ];
    this.innerHTML = `
      <h1>Объявления</h1>
      <ul>${items.map((a) => `<li><b>${a.title}</b><p hidden>${a.details}</p></li>`).join('')}</ul>
      <button>Показать подробности</button>`;
    const button = this.querySelector('button');
    button.onclick = () => {
      const show = this.querySelector('p').hidden;
      this.querySelectorAll('p').forEach((p) => (p.hidden = !show));
      button.textContent = show ? 'Скрыть подробности' : 'Показать подробности';
    };
  }
}

customElements.define('announcements-module', AnnouncementsModule);
