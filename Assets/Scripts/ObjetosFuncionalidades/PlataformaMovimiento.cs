using System.Collections;
using UnityEngine;


public class PlataformaMovimiento : MonoBehaviour
{

    //Este script me es util no solo para plataformas sino tambien para objetos en movimiento y probablemente lo modifique para poder elegir si quiero que sea un bucle o al terminar vuelva al inicio
    //Para poder usarlo en muchos mas casos
    
    [Header("Objeto Para posicion")]//Esta es la posicion objetivo
    public Transform ObposFinal;
    
    //Posiciones iniciales y finales
    private Vector2 posFinal ;
    private Vector2 posInicial;


    [Header("Tiempo del cambio")]
    public float tiempoAnimacion;

    [Header("Curva de animacion del cambio")]
    public AnimationCurve curvaAnimacion;
    
    [Header("Tiempo para volver a moverse")]
    public float tiempoEspera;
    private bool moviendo = false;

    void Start()
    {
        // Al iniciar se establecen la posicion inicial y final
        posInicial = transform.position;
        posFinal = ObposFinal.position;
        moviendo = false;

    }

    
    void FixedUpdate()
    {
        //Si no se esta movimiendo inicia la corutina que recibe como parametro la posicion inicial final y tiempo de animacion
        if ( !moviendo )
        {
            
            StartCoroutine(moverPosicion(posInicial, posFinal, tiempoAnimacion));
        }

       
    }



    IEnumerator moverPosicion(Vector2 posInicio, Vector2 posFin, float duracion)
    {

        moviendo = true;
        float tiempoPasado = 0;
        while (tiempoPasado < duracion)
        {
            
            //Y con el metodo lerp(interpolacion lineal) hago que la posicion vaya variando de un punto a a un punto b
            transform.position = Vector2.Lerp(posInicio,posFin, curvaAnimacion.Evaluate(tiempoPasado/duracion));
            tiempoPasado += Time.fixedUnscaledDeltaTime;
           
            yield return null;
        }
        //No siempre se mueve exactamente a la posicion final sino que varia un poco por eso lo muevo directamente
    
        transform.position = posFin;
        //Funcion que como su nombre lo indica cambia las posiciones, ahora la inicial es la final y viceversa
        cambiarPosiciones();
        yield return new WaitForSeconds(tiempoEspera);
        moviendo = false;
     
    }

    private void cambiarPosiciones() 
    {
        posFinal = posInicial;
        posInicial = transform.position;
    }
}
