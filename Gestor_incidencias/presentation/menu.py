def ejecutar_sistema():
    #Cargar infraestructura
    tecnicos = RepositorioInicial.cargar_tecnicos()
    salas = RepositorioInicial.cargar_salas()
    
    #Iniciar servicios de aplicación
    servicios = ServiciosIncidencias()

    print("=== SISTEMA DE GESTIÓN DE INCIDENCIAS ===")
    
    #Simulación de Flujo: Mañana a Tarde
    t_mañana = tecnicos[0] # Juan
    t_tarde = tecnicos[1]  # Ana
    sala_crisis = salas[0]
    
    print(f"\n[TURNO] Técnico: {t_mañana.nombre} ({t_mañana.turno})")
    
    #El técnico de mañana encuentra una falla
    inc = servicios.nueva_incidencia(101, t_mañana, sala_crisis, "Fallo en  Sala Crisis")
    
    #Termina el turno sin resolverla -> Se genera Borrador Word y aviso para Ana
    print(servicios.generar_documento(inc, tecnico_entrante=t_tarde))

    #Entra el técnico de tarde
    print(f"\n[TURNO] Técnico: {t_tarde.nombre} ({t_tarde.turno})")
    print("Revisando notificaciones de relevo...")
    print(f"Avisos: {t_tarde.notificaciones_pendientes[0]}")
    
    #Ana resuelve la incidencia
    print("\n[ACCION] Ana esta con la incidencia")
    servicios.resolver(inc, "Problema solucionado.")
    
    #Ahora se genera el PDF final
    print(servicios.generar_documento(inc))

if __name__ == "__main__":
    ejecutar_sistema()