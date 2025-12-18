using System.Numerics;
using MathNet.Numerics.IntegralTransforms;

namespace FFTProcessor
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 6)
            {
                Console.WriteLine("Improper arguments");
                Console.WriteLine("Usage: FFTProcessor <inputFile> <outputFile> <numFrames> <height> <width> <samplingRate>");
                return;
            }

            string inputFile = args[0];
            string outputFile = args[1];
            int numFrames = int.Parse(args[2]);
            int height = int.Parse(args[3]);
            int width = int.Parse(args[4]);
            float samplingRate = float.Parse(args[5]);

            int fftLength = numFrames / 2 + 1;

            // Load input data
            float[] data = new float[numFrames * height * width];
            using (var fs = new FileStream(inputFile, FileMode.Open))
            using (var br = new BinaryReader(fs))
            {
                for (int i = 0; i < data.Length; i++)
                    data[i] = br.ReadSingle();
            }

            float[] psdMap = new float[height * width * fftLength];

            // Some stuff for a progress display
            int totalPixels = height * width;
            int rowsCompleted = 0;

            // Parallelize per row for speed
            Console.WriteLine("Starting FFT processing");
            Parallel.For(0, height, row =>
            {
                for (int col = 0; col < width; col++)
                {
                    Complex[] ts = new Complex[numFrames];
                    double mean = 0.0;

                    for (int f = 0; f < numFrames; f++)
                    {
                        float val = data[f * height * width + row * width + col];
                        mean += val;
                        ts[f] = new Complex(val, 0);
                    }
                    mean /= numFrames;

                    for (int f = 0; f < numFrames; f++)
                        ts[f] -= mean;

                    // FFT
                    Fourier.Forward(ts, FourierOptions.Matlab);

                    // Compute PSD (one-sided)
                    for (int i = 0; i < fftLength; i++)
                    {
                        double power = (ts[i].Magnitude * ts[i].Magnitude) / (numFrames * samplingRate);
                        if (i > 0 && i < fftLength - 1) power *= 2; // one-sided correction
                        if (i < 15) power = 0;                      // remove very low freqs
                        psdMap[row * width * fftLength + col * fftLength + i] = (float)power;
                    }
                }

                // Update the progress display
                int doneRows = System.Threading.Interlocked.Increment(ref rowsCompleted);
                int pixelsDone = doneRows * width;

                Console.WriteLine($"Processed {pixelsDone} / {totalPixels} pixels");
                Console.Out.Flush();
            });

            // Write PSD map to binary file
            Console.WriteLine("Finished FFT. Saving results...");
            using (var fs = new FileStream(outputFile, FileMode.Create))
            using (var bw = new BinaryWriter(fs))
            {
                for (int i = 0; i < psdMap.Length; i++)
                    bw.Write(psdMap[i]);
            }

            Console.WriteLine("FFT processing completed!");
        }
    }
}
