var eventosComponent = { delimiters: [], props: [], data: {}, computed: {}, methods: {} };

eventosComponent.delimiters = ["[[", "]]"];

eventosComponent.props = ["opcion", "check-opciones", "eventos", "controles_foco", "datos"]

eventosComponent.data = function () {
    let data = {
        existeEvento: false,
        existeCF: false,
        
    };
    return data;
};

eventosComponent.mounted = function (){
    this.init();    
}

// Methods
eventosComponent.methods = {
    init(){
        $(".custom-select2").select2();
    },
    clase_opcion(opcion) {
        return {
            'current': this.opcion == opcion,
            'disabled': this.opcion != opcion,
            'done': this.checkOpciones[opcion - 1] && this.opcion != opcion
        };
    },
    async incrementarOpcion() {
        const isValidPesquisa = await this.$refs.pesquisaActivaObserver.validate();
        const isValidEventos = await this.$refs.eventosObserver.validate();
        const isValidCF = await this.$refs.cfObserver.validate();
        const isValidMovHospital = await this.$refs.movHospitalObserver.validate();
        
        let continuar = true;
        const mostrarError = () => {
            swal("Error!!", "Existen errores en el formulario.", "error");
            continuar = false;
        };

        switch (parseInt(this.opcion)) {
            case 9:
                if (!isValidPesquisa) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 10:
                if (!isValidEventos) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 11:
                if (!isValidCF) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 12:
                if (!isValidMovHospital) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;

            default:
                break;
        }

        if (continuar) {
            if (!this.checkOpciones[this.opcion - 1]) {
                this.checkOpciones[this.opcion - 1] = true;
            }
            this.$emit('incrementar-opcion');

        }
    },
    decrementarOpcion() {
        this.$emit('decrementar-opcion')
    },
    addEvento() {
        const id_evento = document.querySelector("#selectEventos").value;

        const existe_evento = this.datos.eventos.find((value) => {
            return value.id == id_evento;
        });

        if (!existe_evento) {
            this.existeEvento = false;
            const evento = this.eventos.find((value) => {
                return value.id == id_evento;
            });

            this.datos.eventos.push({
                id: evento.id,
                nombre: evento.nombre,
                cantidad: 0,
            });
        }
        else {
            this.existeEvento = true;
        }
    },
    quitarEvento(key) {
        this.datos.eventos.splice(key, 1);
    },
    addCF() {
        const id_cf = document.querySelector("#selectCF").value;

        const existe_cf = this.datos.controles_foco.find((value) => {
            return value.id == id_cf;
        });

        if (!existe_cf) {
            this.existeCF = false;
            const cf = this.controles_foco.find((value) => {
                return value.id == id_cf;
            });

            this.datos.controles_foco.push({
                id: cf.id,
                nombre: cf.nombre,
                cantidad: 0,
            });
        }
        else {
            this.existeCF = true;
        }
    },
    quitarCF(key) {
        this.datos.controles_foco.splice(key, 1);
    },
};


// Register Component
utils.register_vue_component('eventos', url_eventosComponent, function (template) {
    eventosComponent.template = template.data;
    return eventosComponent;
});