using System.Collections;
using UnityEngine;
using UnityEngine.PlayerLoop;
using UnityEngine.SceneManagement;
using UnityEngine.UIElements;

public class gameManager : MonoBehaviour
{
    //Metodo estatico para poder acceder a este script desde cualquier lado del codigo.
    public static gameManager instance { get; private set; }


    public int FpsJuego = 60;
    //El Hud muestra las vidas y los puntos
    [SerializeField]private HUD hud;
    [Header("Puntajes")]
    public int puntosEscena;
    public int puntosTotales;
    public int monedasUsables;

    [Header("No se destruye al cargar nueva escena")]// Este lo hago para poder probar en cada nivel con un gameManager pero en el exportado final solo habra una instancia de este.
    public bool dontDestroyOnLoad;
    
    private int vidas = 3;
    public float tiempoTranscurrido;
    public float tiempoGuardar;
    //Objeto del jugador
    private GameObject player;
    
    //Variables para guardar checkpoints y Spawnpoints
    private Vector2 checkpoint;
    private Vector2 spawnPoint;

    //Script del jugador
    private movement movement;

    //Objeto de la interfaz
    public GameObject interfaz;
    public GameObject menuOpciones;

    //Arreglo con todas las pantallas de muerte
    public GameObject[] pantallasMuertes;

    //Animaciones de transicion y la del inicio
    public GameObject transicion;
    public GameObject AnimacionInicio;

   //Cantidad de mejoras y si las obtiene
    public int dobleSaltos ;
    public bool canDash;

    //Objeto para guardar los datos.
    public FileManager fileManager;
    
    // Al iniciar se ejecuta este codigo
    private void Start()
    {

        AudioManager.instance.PlayMusic("menu");
        puntosEscena = 0;
        puntosTotales = 0;
        tiempoGuardar = 1000000000000000000000000.00000000000000f;
        //Setea los fps del juego a 60 en un inicio
        Application.targetFrameRate = FpsJuego;

        //Obtiene el elemento del jugador al iniciar y su script
        player = GameObject.FindWithTag("Player");
        movement = player.GetComponent<movement>();

        //Esto es un evento que se ejecutara cada vez que una escena se carga
        SceneManager.sceneLoaded += OnSceneLoaded;

        //Si la escena es la primera desactiva la interfaz
        if (SceneManager.GetActiveScene().buildIndex.Equals(0))
        {
            interfaz.SetActive(false);
        }

        //Instancia el objeto que tiene la animacion al inicio
        Instantiate(AnimacionInicio) ;

        //Carga los datos
        fileManager.CargarData(); 

    }

    //Se ejecuta antes del start
    private void Awake()
    {
        //Si la instancia no existe se crea de lo contrario se destruye, tambien si queremos que no se destruya al cargar una nueva escena
        // Hace que pase eso
        if (instance == null)
        {

            instance = this;

            if (dontDestroyOnLoad)
            {
                DontDestroyOnLoad(gameObject);
            }
           
        }
        else
        {
            Destroy(gameObject);
        }
    }


    //Lo que pasara cada vez que una escena se carga
    void OnSceneLoaded(Scene scene, LoadSceneMode mode)
    {
       //Busca al jugador y su script porque cada escena tiene su objeto jugador
        player = GameObject.FindWithTag("Player");
        movement = player.GetComponent<movement>();
  

        //Activara la interfaz cuando no sea la primera escena de lo contrario reincia todas las variables.
        if (!SceneManager.GetActiveScene().buildIndex.Equals(0))
        {
            interfaz.SetActive(true);
            puntosTotales = puntosTotales + puntosEscena;

            puntosEscena = 0;
        }
        else
        {
            hud.ActualizarPuntos(0);
            hud.activarVida(0); hud.activarVida(1); hud.activarVida(2);
            interfaz.SetActive(false);
            monedasUsables += puntosTotales;
            tiempoTranscurrido = 0;
            puntosEscena = 0;
            puntosTotales = 0;
            vidas = 3;
            
        }

        hud.actualizarSalto(dobleSaltos);
    }

    //Funcion de perder vida recibe si es un enemigo y la cantidad de daño
    public void perderVida(bool enemy, int cantidadDano)
    {
        //Un bucle que se ejecuta n cantidad de daño recibe(maximo 3)
        for (int i = 0; i < cantidadDano; i++) { 
            //Le quita uno de vida
            vidas-=1;
            
            //Si es igual a 0 inicia una corutina pantalla Muerte, reinicia las vidas, los puntos y la posicion del jugador
            if (vidas == 0)
            {
                StartCoroutine(pantallaMuerte());
                player.transform.position = spawnPoint;
                vidas = 3;
                hud.activarVida(0); hud.activarVida(1); hud.activarVida(2);
                puntosEscena = 0;
                hud.ActualizarPuntos(puntosTotales + puntosEscena);
            }

            //Si la vida es diferente de cero, no es enemigo y aparte se encuentra en la ultima iteracion posible(esto por si quiero que al carse quite dos de vida no quiero que se tepee dos veces sino una sola)
            else if (vidas != 0 && !enemy && i == cantidadDano-1)
            {
                //Reinicia la posicion del jugador al chekpoint
                player.transform.position = checkpoint;
                
                //Pequeña penalizacion que resta 10 puntos
                if  (puntosTotales >= 10)
                {
                    puntosTotales -= 10;
                    hud.ActualizarPuntos(puntosTotales);
                }
            
            }

            //Al final de cada iteracion se desactiva en el Hud la vida
            hud.quitarVida(vidas);
        }

    }

    //Corutina de la pantalla de Muerte
    IEnumerator pantallaMuerte()
    {
        //Genera un indice aleatorio lo activa espera cierto tiempo y lo desactiva
        int ind = Random.Range(0, pantallasMuertes.Length);
        AudioManager.instance.PlaySfx("perder");
        pantallasMuertes[ind].SetActive(true);
        yield return new WaitForSeconds(1.2f);
        pantallasMuertes[ind].SetActive(false);
    }


    //Metodo para ganar vida
    public bool ganarVida()
    {
        //Si tienes el numero maximo de vidas no se puede obtener
        if (vidas == 3)
        {
            return false;
        }
        //Activa la vida en el Hud y la suma, retorna falso en caso de que ya tenga 3 vidas porque no quiero mas de 3 vidas
        hud.activarVida(vidas);
        vidas += 1;
        return true;
    }


    //Metodo para sumar puntos, a este metodo accedo desde el script de las monedas
    public void SumarPuntos(int puntosASumar)
    {
        puntosEscena += puntosASumar;
        hud.ActualizarPuntos(puntosEscena + puntosTotales);
    }
    
    //En el update si la escena es diferente de la inicial empieza a contar el tiempo y permite abrir el menu de opciones.

   
    private void Update()
    {
        if (!SceneManager.GetActiveScene().buildIndex.Equals(0))
        {
            if (Input.GetKeyDown(KeyCode.Escape))
            {
                AudioManager.instance.PlaySfx("transicion");
                menuOpciones.SetActive(!menuOpciones.activeSelf);
            }
            tiempoTranscurrido += Time.deltaTime;
            hud.sumarTiempo(tiempoTranscurrido);
        }
    }

    //Guarda la posicion del chekpoint al pasar sobre el, lo uso en otro script
    public void lastCheckpoint(Vector2 posCheckpoint)
    {
        checkpoint = posCheckpoint;
    }

    //Guarda la posicion del Spawnpoint al pasar sobre el, lo referencio en otro script
    public void SpawnPoint(Vector2 pos)
    {
        spawnPoint = pos;
    }
    

    //Metodo para cargar Escenas desde otros scripts
    public void cargarEscena()
    {
        //Corutina de transicion
        StartCoroutine(transition());

    }


    //La corutina de transicion activa la animacion espera un tiempo cambia de escena, espera otro tiempo y hacer la transicion
    IEnumerator transition()
    {

        AudioManager.instance.PlaySfx("transicion");
        transicion.SetActive(true);
        yield return new WaitForSeconds(0.8f);
        if (SceneManager.GetActiveScene().buildIndex.Equals(SceneManager.sceneCountInBuildSettings - 1))
        {
            SceneManager.LoadScene(0);//Si la escena es la ultima va a ir a la primera escena la del menu.
        }
        else
        {
            SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);
        }

        yield return new WaitForSeconds(0.4f);
        if (SceneManager.GetActiveScene().buildIndex.Equals(0))
        {
            Debug.Log("0");
            AudioManager.instance.PlayMusic("menu");
        }
        if (SceneManager.GetActiveScene().buildIndex.Equals(1))
        {
            AudioManager.instance.PlayMusic("nivelMusica");
            Debug.Log("1");
        }
        transicion.SetActive(false);
    }

    

    //Hice todas estas funciones para obtener los elementos  y modificarlos porque estaba teniendo problemas al modificarlos directamente.
    public int getMonedasUsables()
    {
        return monedasUsables;
    }
    
    public void changeMonedasUsables(int cant)
    {
        monedasUsables -= cant;
    }

    public bool getDash()
    {
        return canDash;
    }

    public void changeDash()
    {
        canDash = true;
    }

    public int getDoublejump()
    {
        return dobleSaltos;
    }
    
    public void changeDoublejump()
    {
        dobleSaltos += 3;
    }

    public void usarDobleSalto()
    {
        dobleSaltos -= 1;
        hud.actualizarSalto(dobleSaltos);
       
    }
}
