import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Random;
import javax.swing.*;

public class Destroyer extends JPanel implements ActionListener, KeyListener {
    private Timer timer;
    private Timer moveTimer;
    private int rocketX, rocketY;
    private int rocketWidth = 50, rocketHeight = 50;
    private int lives = 3;
    private boolean gameOver = false;
    private int gameTime = 0; // tempo de jogo em segundos
    private int meteorSpeed = 4; // velocidade inicial dos meteoros
    private int rocketSpeed = 10; // velocidade da nave
    private boolean moveLeft = false, moveRight = false;
    private JButton startButton; // botão para iniciar o jogo
    private JButton restartButton; // botão para reiniciar o jogo
    private ArrayList<Meteor> meteors;
    private Random random;

    // Imagens
    private Image rocketImage;
    private Image meteorImage;
    private Image backgroundGif;

    public Destroyer() {
        this.setFocusable(true);
        SwingUtilities.invokeLater(() -> this.addKeyListener(this));
        this.setPreferredSize(new Dimension(800, 600));

        // Carregar imagens
        rocketImage = new ImageIcon("./assets/2.png").getImage();
        meteorImage = new ImageIcon("./assets/3.png").getImage();
        backgroundGif = new ImageIcon("./assets/1.gif").getImage();

        // Inicializa os meteoros
        meteors = new ArrayList<>();
        random = new Random();

        // Configura o botão de início
        startButton = new JButton("Iniciar Jogo");
        startButton.addActionListener(e -> startGame());
        this.add(startButton);

        // Configura o botão de reinício
        restartButton = new JButton("Reiniciar Jogo");
        restartButton.addActionListener(e -> restartGame());
        restartButton.setVisible(false);
        this.add(restartButton);
    }

    private void startGame() {
        rocketX = 375;
        rocketY = 500;
        lives = 3;
        gameTime = 0;
        gameOver = false;
        meteors.clear();

        // Configura o timer principal
        if (timer != null) {
            timer.stop();
        }
        timer = new Timer(1000, e -> gameTime++); // Incrementa o tempo de jogo a cada segundo
        timer.start();

        // Cria meteoros a cada segundo
        new Timer(1000, e -> addMeteor()).start();

        // Configura o timer de movimento da nave e atualização do jogo
        if (moveTimer != null) {
            moveTimer.stop();
        }
        moveTimer = new Timer(16, this); // Atualiza a cada 16ms (~60 FPS)
        moveTimer.start();

        startButton.setVisible(false);
        restartButton.setVisible(false);
    }

    private void restartGame() {
        startGame();
    }

    private void addMeteor() {
        int x = random.nextInt(getWidth() - rocketWidth);
        int y = -rocketHeight;
        meteors.add(new Meteor(x, y, rocketWidth, rocketHeight));
    }

    private void updateRocketPosition() {
        if (moveLeft && rocketX > 0) {
            rocketX -= rocketSpeed;
        }
        if (moveRight && rocketX < getWidth() - rocketWidth) {
            rocketX += rocketSpeed;
        }
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Desenhar o fundo
        g.drawImage(backgroundGif, 0, 0, getWidth(), getHeight(), this);

        // Desenhar o foguete
        g.drawImage(rocketImage, rocketX, rocketY, rocketWidth, rocketHeight, this);

        // Desenhar os meteoros
        for (Meteor meteor : meteors) {
            g.drawImage(meteorImage, meteor.x, meteor.y, meteor.width, meteor.height, this);
        }

        // Desenhar o tempo de jogo
        int minutes = gameTime / 60;
        int seconds = gameTime % 60;
        String timeString = String.format("%02d:%02d", minutes, seconds);
        g.setColor(Color.WHITE);
        g.setFont(new Font("Arial", Font.BOLD, 20));
        g.drawString(timeString, 10, 20);

        // Desenhar vidas
        g.drawString("Vidas: " + lives, 10, 40);

        // Desenhar mensagem de game over
        if (gameOver) {
            g.setFont(new Font("Arial", Font.BOLD, 50));
            g.setColor(Color.RED);
            g.drawString("Game Over", getWidth() / 2 - 150, getHeight() / 2);
            restartButton.setVisible(true);
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (!gameOver) {
            // Atualiza a posição dos meteoros
            Iterator<Meteor> iterator = meteors.iterator();
            while (iterator.hasNext()) {
                Meteor meteor = iterator.next();
                meteor.y += meteorSpeed;
                if (meteor.y > getHeight()) {
                    iterator.remove();
                } else if (meteor.intersects(rocketX, rocketY, rocketWidth, rocketHeight)) {
                    lives--;
                    iterator.remove();
                    if (lives <= 0) {
                        gameOver = true;
                        timer.stop();
                        moveTimer.stop();
                    }
                }
            }

            // Atualiza a posição do foguete
            updateRocketPosition();

            // Redesenha o painel
            repaint();
        }
    }

    @Override
    public void keyPressed(KeyEvent e) {
        int key = e.getKeyCode();
        if (key == KeyEvent.VK_LEFT) {
            moveLeft = true;
        }
        if (key == KeyEvent.VK_RIGHT) {
            moveRight = true;
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {
        int key = e.getKeyCode();
        if (key == KeyEvent.VK_LEFT) {
            moveLeft = false;
        }
        if (key == KeyEvent.VK_RIGHT) {
            moveRight = false;
        }
    }

    @Override
    public void keyTyped(KeyEvent e) {}

    public static void main(String[] args) {
        JFrame frame = new JFrame("Destroyer");
        Destroyer game = new Destroyer();
        frame.add(game);
        frame.pack();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }

    private static class Meteor {
        int x, y, width, height;

        Meteor(int x, int y, int width, int height) {
            this.x = x;
            this.y = y;
            this.width = width;
            this.height = height;
        }

        boolean intersects(int rx, int ry, int rwidth, int rheight) {
            Rectangle meteorRect = new Rectangle(x, y, width, height);
            Rectangle rocketRect = new Rectangle(rx, ry, rwidth, rheight);
            return meteorRect.intersects(rocketRect);
        }
    }
}