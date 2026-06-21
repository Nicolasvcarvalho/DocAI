export function Button({texto, carregando, textoCarregando}){

    const styles = {
        button: {
        width: '100%',
        padding: '12px',
        backgroundColor: '#3b82f6',
        color: '#fff',
        border: 'none',
        borderRadius: '8px',
        fontSize: '15px',
        fontWeight: '600',
        cursor: 'pointer',
        marginTop: '8px',},
        buttonDisabled: {
        opacity: 0.6,
        cursor: 'not-allowed',},
    };
        return (
            <button
            type="submit"
            style={{
              ...styles.button,
              ...(carregando ? styles.buttonDisabled : {}),
            }}
            disabled={carregando}
          >
            {carregando ? textoCarregando : texto}
          </button>
        )
      

}