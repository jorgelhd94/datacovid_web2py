var vigilanciaComponent = { delimiters: [], props: [], data: {}, computed: {}, methods: {} };

vigilanciaComponent.delimiters = ["[[", "]]"];

vigilanciaComponent.props = ["opcion", "check-opciones", "origenes", "datos"]

vigilanciaComponent.data = function () {
    let data = {
        existeOrigen: false,
        
    };
    return data;
};

vigilanciaComponent.mounted = function (){
    this.init();    
}

// Methods
vigilanciaComponent.methods = {
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
        const isValidVigilancia = await this.$refs.vigilanciaObserver.validate();
        const isValidOrigen = await this.$refs.origenObserver.validate();
        const isValidPendientes = await this.$refs.pendientesObserver.validate();
        const isValidInspeccion = await this.$refs.inspeccionObserver.validate();
        
        let continuar = true;
        const mostrarError = () => {
            swal("Error!!", "Existen errores en el formulario.", "error");
            continuar = false;
        };

        switch (parseInt(this.opcion)) {
            case 13:
                if (!isValidVigilancia) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 14:
                if (!isValidOrigen) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 15:
                if (!isValidPendientes) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 16:
                if (!isValidInspeccion) {
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
    addOrigen() {
        const id_origen = document.querySelector("#selectOrigen").value;

        const existe_origen = this.datos.vigilancia.origen.find((value) => {
            return value.id == id_origen;
        });

        if (!existe_origen) {
            this.existeOrigen = false;
            const origen = this.origenes.find((value) => {
                return value.id == id_origen;
            });

            this.datos.vigilancia.origen.push({
                id: origen.id,
                nombre: origen.nombre,
                cantidad: 0,
            });
        }
        else {
            this.existeOrigen = true;
        }
    },
    quitarOrigen(key) {
        this.datos.vigilancia.origen.splice(key, 1);
    },
};


// Register Component
utils.register_vue_component('vigilancia', url_vigilanciaComponent, function (template) {
    vigilanciaComponent.template = template.data;
    return vigilanciaComponent;
});