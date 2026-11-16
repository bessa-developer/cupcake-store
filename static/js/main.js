/* Interações do front da loja. Sem JavaScript as páginas continuam
   funcionando, isto só melhora a experiência. */
(function () {
  'use strict';

  document.documentElement.classList.add('com-js');

  /* Menu no celular */
  var botaoMenu = document.querySelector('.menu-botao');
  var nav = document.getElementById('nav-principal');

  if (botaoMenu && nav) {
    botaoMenu.addEventListener('click', function () {
      var aberto = nav.classList.toggle('aberto');
      botaoMenu.setAttribute('aria-expanded', aberto ? 'true' : 'false');
    });

    nav.addEventListener('click', function (e) {
      if (e.target.closest('a') && nav.classList.contains('aberto')) {
        nav.classList.remove('aberto');
        botaoMenu.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('aberto')) {
        nav.classList.remove('aberto');
        botaoMenu.setAttribute('aria-expanded', 'false');
        botaoMenu.focus();
      }
    });
  }

  /* Fechar mensagens de retorno */
  function someMensagem(msg) {
    msg.style.transition = 'opacity .18s ease, transform .18s ease';
    msg.style.opacity = '0';
    msg.style.transform = 'translateY(-6px)';
    setTimeout(function () { msg.remove(); }, 180);
  }

  document.addEventListener('click', function (e) {
    var fechar = e.target.closest('.mensagem .fechar');
    if (fechar) {
      someMensagem(fechar.closest('.mensagem'));
    }
  });

  /* As mensagens também desaparecem sozinhas depois de alguns segundos,
     sem tirar o botão de fechar, que continua funcionando na hora. */
  document.querySelectorAll('.mensagem').forEach(function (msg, i) {
    setTimeout(function () {
      if (msg.isConnected) someMensagem(msg);
    }, 5000 + i * 600);
  });

  /* Seletores de quantidade */
  document.querySelectorAll('[data-quantidade]').forEach(function (form) {
    var entrada = form.querySelector('input[name="quantidade"]');
    if (!entrada) return;

    var min = parseInt(entrada.min, 10) || 1;
    var max = parseInt(entrada.max, 10) || 99;
    var enviaAoMudar = form.hasAttribute('data-enviar-ao-mudar');

    function ajusta(delta) {
      var atual = parseInt(entrada.value, 10);
      if (isNaN(atual)) atual = min;
      var novo = Math.min(max, Math.max(min, atual + delta));
      if (novo !== atual) {
        entrada.value = novo;
        entrada.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }

    var menos = form.querySelector('.menos');
    var mais = form.querySelector('.mais');
    if (menos) menos.addEventListener('click', function () { ajusta(-1); });
    if (mais) mais.addEventListener('click', function () { ajusta(1); });

    entrada.addEventListener('blur', function () {
      var v = parseInt(entrada.value, 10);
      if (isNaN(v) || v < min) entrada.value = min;
      if (v > max) entrada.value = max;
    });

    /* No carrinho, mudar a quantidade já envia a atualização e dispensa o botão */
    if (enviaAoMudar) {
      var botaoEnviar = form.querySelector('.sem-js');
      if (botaoEnviar) botaoEnviar.style.display = 'none';

      var tempo;
      entrada.addEventListener('change', function () {
        clearTimeout(tempo);
        tempo = setTimeout(function () { form.submit(); }, 350);
      });
    }
  });

  /* Destaca a forma de pagamento marcada */
  var opcoesForma = document.querySelectorAll('.forma input[type="radio"]');
  if (opcoesForma.length) {
    function sincronizaFormas() {
      opcoesForma.forEach(function (radio) {
        radio.closest('.forma').classList.toggle('selecionada', radio.checked);
      });
    }
    opcoesForma.forEach(function (radio) {
      radio.addEventListener('change', sincronizaFormas);
    });
    sincronizaFormas();
  }

  /* Confirmação antes de remover no admin */
  document.querySelectorAll('form[data-confirmar]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!window.confirm(form.getAttribute('data-confirmar'))) {
        e.preventDefault();
      }
    });
  });
})();
