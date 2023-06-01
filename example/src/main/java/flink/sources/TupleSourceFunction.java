
package flink.sources;

import org.apache.flink.api.java.tuple.Tuple4;
import org.apache.flink.streaming.api.functions.source.RichParallelSourceFunction;

import java.util.Date;
import java.util.List;
import java.util.Random;

/**
 * A ParallelSourceFunction that generates a Tuple4<Long, Long, Long, Long>
 */
public class TupleSourceFunction extends RichParallelSourceFunction<Tuple4<Long, Long, Long, Long>> {

    private volatile boolean running = true;
    private long eventsCountSoFar = 0;
    private final Integer rate;

    public TupleSourceFunction(Integer srcRate) {
        this.rate = srcRate;
    }

    @Override
    public void run(SourceContext<Tuple4<Long, Long, Long, Long>> ctx) throws Exception {
        while (running) {
            long emitStartTime = System.currentTimeMillis();

            for (int i = 0; i < rate; i++) {
                Random rnd = new Random();
                long kk=rnd.nextLong();
                long vv=rnd.nextLong();

                ctx.collect(Tuple4.of(kk,vv,kk,vv));
                eventsCountSoFar++;
            }

            // Sleep for the rest of timeslice if needed
            long emitTime = System.currentTimeMillis() - emitStartTime;
            if (emitTime < 1000) {
                Thread.sleep(1000 - emitTime);
            }
        }
    }

    @Override
    public void cancel() {
        running = false;
    }

}
