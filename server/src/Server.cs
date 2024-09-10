namespace src;

public class Server {
    public Server() {
        var con = new NpgsqlConnection(connectionString: "";)
        con.Open();
        using var cmd = new NpgsqlCommand();
        cmd.Connection = con;
    }
}
