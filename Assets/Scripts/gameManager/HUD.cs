using UnityEngine;
using TMPro;
using System.Diagnostics.SymbolStore;

public class HUD : MonoBehaviour
{
    //Script del hud
    //Estos objetos de TextMeshPro son los textos de la interfaz, puntos y tiempo
    private TextMeshProUGUI puntos;
    private TextMeshProUGUI time;
    public TextMeshProUGUI numSaltos;
    //Los objetos que contienen a los elementos de texto
    private GameObject tiempo;
    private GameObject Money;
    [Header("Elento Vida Ui")]
    public GameObject[] vidas;
    

    private void Start()
    {
        //Al inciar la escena encuentra los elemtos que contienen los textos y a los textos
        Money = GameObject.FindWithTag("money");
        puntos = Money.GetComponent<TextMeshProUGUI>();
        tiempo = GameObject.FindWithTag("time");
        time = tiempo.GetComponent<TextMeshProUGUI>();
    }

    //La funcion sumar tiempo recibe un flotante de tiempo
    public void sumarTiempo(float tiempo)
    {
        //Esto muestra los minutos segundos y milisegundos
        int minutes = Mathf.FloorToInt(tiempo / 60);
        int seconds = Mathf.FloorToInt(tiempo % 60);
        int milliseconds = Mathf.FloorToInt((tiempo * 1000) % 1000);
        time.text = $"{minutes:00}:{seconds:00}:{milliseconds:000}";
 
    }

    //Actualiza los puntos en la interfaz.
    public void ActualizarPuntos(int puntosTotales)
    {
        puntos.text = puntosTotales.ToString();
    }

    //Actualiza la vida en la interfaz
    public void quitarVida(int indice)
    {
        vidas[indice].SetActive(false);
    }


    public void actualizarSalto(int saltos)
    {
        Debug.Log(saltos);
        numSaltos.text = saltos.ToString();
    }
    public void activarVida(int indice)
    {
        vidas[indice].SetActive(true);
    }
}
