var sospechaComponent = { delimiters: [], props: [], data: {}, computed: {}, methods: {} };

sospechaComponent.delimiters = ["[[", "]]"];

sospechaComponent.props = ["opcion", "check-opciones", "datos"]

sospechaComponent.data = function () {
    let data = {
        
    };
    return data;
};


// Methods
sospechaComponent.methods = {
    clase_opcion(opcion) {
        return {
            'current': this.opcion == opcion,
            'disabled': this.opcion != opcion,
            'done': this.checkOpciones[opcion - 1] && this.opcion != opcion
        };
    },
    async incrementarOpcion() {
        const isValidFallecidos = await this.$refs.fallecidosObserver.validate();
        const isValidSospechosos = await this.$refs.sospechososObserver.validate();
        const isValidCasosIRA = await this.$refs.casosIRAObserver.validate();
        const isValidAtencionIRA = await this.$refs.atencionIRAObserver.validate();
        
        let continuar = true;
        const mostrarError = () => {
            swal("Error!!", "Existen errores en el formulario.", "error");
            continuar = false;
        };

        switch (parseInt(this.opcion)) {
            case 5:
                if (!isValidFallecidos) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 6:
                if (!isValidSospechosos) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 7:
                if (!isValidCasosIRA) {
                    // Se activa si ocurre un error en el formulario
                    mostrarError();
                }
                break;
            case 8:
                if (!isValidAtencionIRA) {
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
};


// Register Component
utils.register_vue_component('sospecha', url_sospechaComponent, function (template) {
    sospechaComponent.template = template.data;
    return sospechaComponent;
});