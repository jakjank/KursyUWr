public class krol implements karty
{
    @Override
    public int wartosc()
    {
        return 13;
    }
    
    @Override
    public int compareTo(karty karta)
    {
        return Integer.compare(this.wartosc(), karta.wartosc());
    }

}
