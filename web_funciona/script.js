document.addEventListener("DOMContentLoaded", function() {
    const gallina = document.getElementById('gallina');
    const zorro = document.getElementById('zorro');
    const semillas = document.getElementById('semillas');
    const bote = document.getElementById('bote');
    const frame1 = document.getElementById('frame1');
    const frame2 = document.getElementById('frame2');
    const frame3 = document.getElementById('frame3');

    // Función para animar el movimiento del bote de izquierda a derecha
    function animateBoteRight() {
        const frameWidth = frame2.offsetWidth;
        const boteWidth = bote.offsetWidth;
        const boteLeft = bote.offsetLeft;
        const targetLeft = frameWidth - boteWidth - 10; // Ajuste de margen derecho

        const animation = bote.animate(
        [{ left: boteLeft + 'px' }, { left: targetLeft + 'px' }],
        { duration: 1000 }
        );

        animation.onfinish = function() {
            // Mover el ícono seleccionado al frame derecho
            const selectedIcon = frame2.querySelector('.selected');
            if (selectedIcon) {
                selectedIcon.classList.remove('selected');
                frame3.appendChild(selectedIcon);
                // Verificar si el bote debe quedarse en el lado derecho del frame2
                if (bote.offsetLeft >= targetLeft) {
                    frame2.appendChild(bote);
                }
                // Verificar la validez de la situación
                checkSituation();
            }
        };
    }

    // Función para animar el movimiento del bote de derecha a izquierda
    function animateBoteLeft() {
        const frameWidth = frame2.offsetWidth;
        const boteWidth = bote.offsetWidth;
        const boteLeft = bote.offsetLeft;
        const targetLeft = 10; // Ajuste de margen izquierdo

        const animation = bote.animate(
        [{ left: boteLeft + 'px' }, { left: targetLeft + 'px' }],
        { duration: 1000 }
        );
        
        animation.onfinish = function() {
            // Mover el ícono seleccionado al frame izquierdo
            const selectedIcon = frame2.querySelector('.selected');
            if (selectedIcon) {
                selectedIcon.classList.remove('selected');
                frame1.appendChild(selectedIcon);
                // Verificar si el bote debe quedarse en el lado izquierdo del frame2
                if (bote.offsetLeft < targetLeft) {
                    frame2.appendChild(bote);
                }
                // Verificar la validez de la situación
                checkSituation();
            }
        };
    }

// Función para verificar la validez de la situación
function checkSituation() {
    // Verificar si la gallina y las semillas están solas en algún lado
    const ladoIzquierdo = frame1.children.length > 1;
    const ladoDerecho = frame3.children.length > 1;
    const boteEnElMedio = frame2.children.length > 1;

    if ((gallina.parentNode && gallina.parentNode.id === 'frame1') &&
        (semillas.parentNode && semillas.parentNode.id === 'frame1') &&
        (!zorro.parentNode || zorro.parentNode.id !== 'frame1')) {
        alert("¡Has perdido! La gallina se ha comido las semillas.");
    } else if ((gallina.parentNode && gallina.parentNode.id === 'frame3') &&
        (semillas.parentNode && semillas.parentNode.id === 'frame3') &&
        (!zorro.parentNode || zorro.parentNode.id !== 'frame3')) {
        alert("¡Has perdido! La gallina se ha comido las semillas.");
    } else if (gallina.parentNode && semillas.parentNode && gallina.parentNode === semillas.parentNode) {
        alert("¡Has perdido! La gallina se ha comido las semillas.");
    } else if (gallina.parentNode && zorro.parentNode && gallina.parentNode === zorro.parentNode) {
        alert("¡Has perdido! El zorro se ha comido la gallina.");
    } else if (ladoIzquierdo && ladoDerecho && !boteEnElMedio) {
        alert("¡Has ganado! Has llevado a la gallina, al zorro y las semillas al otro lado sin que se coman entre ellos.");
    }
}



    // Agregar evento de clic para mover el bote al lado opuesto y quedarse en su nueva posición
    bote.addEventListener('click', function() {
        // Determinar la posición actual del bote
        const boteLeft = bote.offsetLeft;
        const frameWidth = frame2.offsetWidth;
        const targetLeft = frameWidth - bote.offsetWidth - 10; // Ajuste de margen derecho
        // Si el bote está en el lado izquierdo, animarlo hacia la derecha
        if (boteLeft < targetLeft) {
            animateBoteRight();
            // Quedarse en la nueva posición
            bote.style.left = targetLeft + 'px';
        } else { // Si el bote está en el lado derecho, animarlo hacia la izquierda
            animateBoteLeft();
            // Quedarse en la nueva posición
            bote.style.left = '10px'; // Ajuste de margen izquierdo
        }
    });

    // Agregar evento de arrastre para cada icono
    [gallina, zorro, semillas, bote].forEach(icon => {
        icon.addEventListener('dragstart', function(e) {
            // Configurar los datos de transferencia para el ícono arrastrado
            e.dataTransfer.setData('text/plain', icon.id);
            // Si es un ícono seleccionable, agregar la clase 'selected' para destacarlo
            if ([gallina, zorro, semillas].includes(icon)) {
                icon.classList.add('selected');
            }
        });
    });

    // Agregar eventos de soltura para el bote solo en el frame del río
    frame2.addEventListener('dragover', function(e) {
        e.preventDefault();
    });

    frame2.addEventListener('drop', function(e) {
        e.preventDefault();
        const iconId = e.dataTransfer.getData('text/plain');
        const icon = document.getElementById(iconId);
        // Verificar si el elemento arrastrado es un ícono
        if (icon && icon !== frame2) {
            // Mover el ícono al bote si no es el bote mismo
            if (icon === bote) {
                frame2.appendChild(bote);
                // Mover los otros íconos junto al bote
                [gallina, zorro, semillas].forEach(icon => frame2.appendChild(icon));
            } else {
                frame2.appendChild(icon);
            }
            // Animar el movimiento del bote hacia la derecha
            //animateBoteRight();
        }
    });

    // Agregar evento de clic para seleccionar un ícono
    [gallina, zorro, semillas].forEach(icon => {
        icon.addEventListener('click', function() {
            // Remover la clase de selección de todos los íconos
            [gallina, zorro, semillas].forEach(i => i.classList.remove('selected'));
            // Agregar la clase de selección al ícono clicado
            icon.classList.add('selected');
        });
    });
});


