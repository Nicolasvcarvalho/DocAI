export function Logo() {
  const styles = {
    logo: {
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      marginBottom: '8px',
    },
    logoIcon: {
      width: '36px',
      height: '36px',
      backgroundColor: '#3b82f6',
      borderRadius: '8px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: '#fff',
      fontSize: '18px',
      fontWeight: 'bold',
    },
    logoText: {
      color: '#fff',
      fontSize: '20px',
      fontWeight: 'bold',
    },
  };

  return (
    <div style={styles.logo}>
      <div style={styles.logoIcon}>D</div>
      <span style={styles.logoText}>DocAI</span>
    </div>
  );
}