document.addEventListener("DOMContentLoaded", function () {
    // 1. Phone number masking logic
    const phoneInputs = document.querySelectorAll(".phone-mask");

    phoneInputs.forEach(function (input) {
        // Formata o valor inicial (se houver)
        if (input.value) {
            input.value = formatPhone(input.value);
        }

        input.addEventListener("input", function () {
            input.value = formatPhone(input.value);
        });
    });

    function formatPhone(value) {
        let cleanValue = value.replace(/\D/g, "");

        if (cleanValue.length > 11) {
            cleanValue = cleanValue.slice(0, 11);
        }

        if (cleanValue.length <= 10) {
            return cleanValue.replace(/^(\d{0,2})(\d{0,4})(\d{0,4}).*/, function (_, ddd, part1, part2) {
                let result = "";
                if (ddd) result += "(" + ddd;
                if (ddd.length === 2) result += ") ";
                if (part1) result += part1;
                if (part2) result += "-" + part2;
                return result;
            });
        } else {
            return cleanValue.replace(/^(\d{0,2})(\d{0,5})(\d{0,4}).*/, function (_, ddd, part1, part2) {
                let result = "";
                if (ddd) result += "(" + ddd;
                if (ddd.length === 2) result += ") ";
                if (part1) result += part1;
                if (part2) result += "-" + part2;
                return result;
            });
        }
    }

    // 2. Public Appointment Booking Flow Interaction
    const barberSelect = document.querySelector('select[name="barbeiro"]');
    const dateInput = document.querySelector('input[name="data"]');
    const serviceSelect = document.querySelector('select[name="servico"]');
    const timeGridContainer = document.getElementById("time-grid-container");
    const hiddenTimeInput = document.getElementById("id_horario_input");
    const summaryCard = document.getElementById("booking-summary");

    if (barbeiroSelect && dateInput && timeGridContainer) {
        barberSelect.addEventListener("change", fetchAvailableTimes);
        dateInput.addEventListener("change", fetchAvailableTimes);
        if (serviceSelect) {
            serviceSelect.addEventListener("change", updateSummary);
        }

        // Set minimum date to today
        const todayStr = new Date().toISOString().split('T')[0];
        dateInput.setAttribute("min", todayStr);

        function fetchAvailableTimes() {
            const barberId = barberSelect.value;
            const selectedDate = dateInput.value;

            if (!barberId || !selectedDate) {
                timeGridContainer.innerHTML = `
                    <div class="text-center text-muted py-3">
                        <i class="bi bi-info-circle fs-4 d-block mb-2"></i>
                        Selecione um barbeiro e uma data para ver os horários.
                    </div>`;
                return;
            }

            timeGridContainer.innerHTML = `
                <div class="text-center py-3 text-success">
                    <div class="spinner-border spinner-border-sm mb-2" role="status"></div>
                    <span class="d-block">Buscando horários disponíveis...</span>
                </div>`;

            // Reset time input and summary
            if (hiddenTimeInput) hiddenTimeInput.value = "";
            updateSummary();

            fetch(`/horarios-disponiveis/?barbeiro=${barberId}&data=${selectedDate}`)
                .then(response => {
                    if (!response.ok) throw new Error("Erro ao carregar horários.");
                    return response.json();
                })
                .then(data => {
                    renderTimeSlots(data.times);
                })
                .catch(err => {
                    console.error(err);
                    timeGridContainer.innerHTML = `
                        <div class="text-center text-danger py-3">
                            <i class="bi bi-exclamation-triangle fs-4 d-block mb-2"></i>
                            Não foi possível carregar os horários. Tente novamente.
                        </div>`;
                });
        }

        function renderTimeSlots(times) {
            if (!times || times.length === 0) {
                timeGridContainer.innerHTML = `
                    <div class="text-center text-warning py-3">
                        Sem horários disponíveis para esta data.
                    </div>`;
                return;
            }

            timeGridContainer.innerHTML = "";
            const grid = document.createElement("div");
            grid.className = "time-grid";

            times.forEach(slot => {
                const btn = document.createElement("button");
                btn.type = "button";
                btn.className = "time-slot-btn";
                btn.innerText = slot.time;
                btn.disabled = !slot.available;

                btn.addEventListener("click", function () {
                    document.querySelectorAll(".time-slot-btn").forEach(b => b.classList.remove("selected"));
                    btn.classList.add("selected");
                    if (hiddenTimeInput) {
                        hiddenTimeInput.value = slot.time;
                    }
                    updateSummary();
                });

                grid.appendChild(btn);
            });

            timeGridContainer.appendChild(grid);
        }

        function updateSummary() {
            if (!summaryCard) return;

            const serviceName = serviceSelect ? serviceSelect.options[serviceSelect.selectedIndex]?.text : "";
            const barberName = barberSelect.options[barberSelect.selectedIndex]?.text || "";
            const selectedDate = dateInput.value;
            const selectedTime = hiddenTimeInput ? hiddenTimeInput.value : "";

            if (!serviceName && !barberName && !selectedDate && !selectedTime) {
                summaryCard.innerHTML = `
                    <p class="text-muted text-center mb-0">
                        Preencha as informações para ver o resumo aqui.
                    </p>`;
                return;
            }

            let formattedDate = "";
            if (selectedDate) {
                const parts = selectedDate.split("-");
                if (parts.length === 3) {
                    formattedDate = `${parts[2]}/${parts[1]}/${parts[0]}`;
                }
            }

            summaryCard.innerHTML = `
                <ul class="list-unstyled mb-0">
                    <li class="mb-2"><strong>Serviço:</strong> <span class="text-success">${serviceName || 'Não selecionado'}</span></li>
                    <li class="mb-2"><strong>Barbeiro:</strong> <span>${barberName || 'Não selecionado'}</span></li>
                    <li class="mb-2"><strong>Data:</strong> <span>${formattedDate || 'Não selecionada'}</span></li>
                    <li class="mb-0"><strong>Horário:</strong> <span class="badge badge-delacruz">${selectedTime || 'Não selecionado'}</span></li>
                </ul>
            `;
        }
    }
});
